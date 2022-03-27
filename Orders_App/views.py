import random

from .interconnect import send_request_post
from rest_framework.exceptions import ValidationError
from Orders_App.models import *
from django.views.decorators.csrf import csrf_exempt
from Orders_App.serializers import OrderSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse, JsonResponse
from rest_framework import renderers
import json
import datetime
from OrdersApp.settings import DELIVERY_MICROSERVICE_URL, STORES_MICROSERVICE_URL, USERS_MICROSERVICE_URL


# To laod environment variables

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'orders': reverse('order-list', request=request, format=format)
    })


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        number = str(self.request.headers['user-phone-number'])
        token = self.request.headers['Token']
        num = str(number)
        if token:
            if len(num) == 10:
                return Order.objects.all()
            else:
                print("Invalid request")
                raise ValidationError('Phone number invalid')
        else:
            raise ValidationError('Token not provided')

    def perform_create(self, serializer):
        cost = 0
        url = STORES_MICROSERVICE_URL + '/order_summary/'
        succ, resp = send_request_post(url, {"item_list":self.request.POST.get("item_list")})
        if not succ:
            raise ValidationError("/order_summary : Could not connect to stores microservices")
        else:
            resp = resp.json()
            cost = resp['total_cost']        

            item_list = []
            items = resp['item_list']
            for item in items:
                item_list.append(Item.objects.create(itemId=item["item"],name=item["name"], quantity=item["quantity"], item_price=item["item_price"]))

        # call Order Validation API
        body = {'store_id': self.request.POST.get("store_id"),
                'item_list': self.request.POST.get("item_list"),
                'customer': self.request.POST.get("customer"),
                'transaction_token': self.request.POST.get("transaction_token")}
        url = STORES_MICROSERVICE_URL+'/verify_order/'
        success, response = send_request_post(url, body)
        if not success:
            raise ValidationError("/verify_order : Could not connect to stores microservices")
        response = response.json()
        if response['msg'] == 'true':
            serializer.save(items=item_list, order_time=datetime.time, delivery_otp=random.randint(100000, 999999), cost=cost, store_name=response["store_name"])
        else:
            raise ValidationError("Order Could not be placed ")


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        item_list = Order.objects.get(pk=self.kwargs['pk']).items.all()
        new_item_list = []
        if self.request.POST.get("customer"):
            serializer.customer = self.request.POST.get("customer")
        if self.request.POST.get("transaction_token"):
            serializer.transaction_token = self.request.POST.get("transaction_token")
        if self.request.POST.get("item_list"):
            items = json.loads(self.request.POST.get("item_list"))
            for item in items:
                try:
                    temp = Item.objects.create(itemId=item["item"], quantity=item["quantity"])
                    new_item_list.append(temp)
                except Exception as e1:
                    ValidationError(e1)
        item_list = new_item_list
        try:
            serializer.save(items=item_list)
        except Exception as e:
            ValidationError(e)


class OrderCancel(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.delivery_status = Order_status[4]
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class ReviewDetails(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        return Response({
            'order_id': order.id,
            'review_text': order.review_text,
            'review_score': order.review_score
        })

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.review_text = request.POST.get('review_text')
        order.review_score = request.POST.get('review_score')
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class VerifyOTP(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        success_message = 'OTP VERIFICATION SUCCESFULL'
        failure_message = 'Entered OTP is incorrect'
        if request.POST.get('delivery_otp') == str(order.delivery_otp):
            order.delivery_status= Order_status[3]
            order.save()
            return Response({'Message ': success_message, 'otpverification_status': True, }, status=status.HTTP_200_OK)
        else:
            return Response({'Message': failure_message, 'otpverification_status': False},
                            status=status.HTTP_404_NOT_FOUND)


class UpdateOrderStatus(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        """
        0 - Pending
        1 - Accepted
        2 - Out-for-delivery
        3 - Delivered
        4 - Canceled
        """
        target_status = int(request.POST.get("target_status"))
        if 0 <= target_status < 5:
            order.delivery_status = Order_status[target_status]
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            raise ValidationError("Invalid status code")

@api_view(["GET"])
def pastOrders(request):
    user_id = request.data['user_id']
    orders = Order.objects.filter(customer=user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

