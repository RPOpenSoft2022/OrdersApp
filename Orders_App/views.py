import random

from .interconnect import send_request_post, send_request_get
import razorpay
from rest_framework.exceptions import ValidationError
from Orders_App.models import *
from rest_framework import viewsets
from Orders_App.serializers import OrderSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse, JsonResponse
from rest_framework import renderers
import json, jwt
import datetime
import requests
from OrdersApp.settings import DELIVERY_MICROSERVICE_URL, STORES_MICROSERVICE_URL, USERS_MICROSERVICE_URL

month_code = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# To laod environment variables

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'orders': reverse('order-list', request=request, format=format)
    })


class OrderList(APIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(self.request.data)
        cost = 0
        url = STORES_MICROSERVICE_URL + '/order_summary/'
        succ, resp = send_request_post(url, {"item_list": self.request.data["item_list"]})
        if not succ:
            raise ValidationError("/order_summary : Could not connect to stores microservices")
        else:
            # resp = resp.json()
            cost = resp['total_cost']

            item_list = []
            items = resp['item_list']
            for item in items:
                item_list.append(Item.objects.create(itemId=item["id"], name=item["name"], quantity=item["quantity"],
                                                     item_price=item["price"]))

        # call Order Validation API
        body = {'store_id': self.request.data["store_id"],
                'item_list': self.request.data["item_list"]}
        print(body)
        url = STORES_MICROSERVICE_URL + '/verify_order/'
        success, response = send_request_post(url, body)
        if not success:
            raise ValidationError("/verify_order : Could not connect to stores microservices")
        response = response.json()
        if response['msg'] == 'true':
            client = razorpay.Client(auth=("rzp_test_VQzdw3Uw16TNCX", "28FFWy85MFzJPr8BDERerR3K"))
            DATA = {
                "amount": cost*100,
                "currency": "INR"
            }
            payment = client.order.create(data=DATA)
            if payment["id"]:
                data = {
                    'items': item_list,
                    'order_time': datetime.time,
                    'delivery_otp': random.randint(100000, 999999),
                    'cost': cost,
                    'store_name': response["store_name"],
                    'transaction_token': payment["id"]
                }
                customer = jwt.decode(self.request.data['token'],
                                      "django-insecure--&l&@&=367*&9v_agoyln$dk&*4(u$a-7orvvr@^scp8^62cs*",
                                      algorithms=["HS256"])['id']
                # data = {
                #     "items": item_list,
                #     "order_time": datetime.time,
                #     "delivery_otp": random.randint(100000, 999999),
                #     "delivery_address": request.data["delivery_address"],
                #     "cost": cost,
                #     "store_id": request.data["store_id"],
                #     "store_name": response['store_name'],
                #     "transaction_token": payment["id"],
                #     "customer": customer
                # }
                order = Order.objects.create(delivery_otp=random.randint(100000, 999999),
                                             delivery_address=request.data["delivery_address"], cost=cost,
                                             store_id=request.data["store_id"], store_name=response['store_name'],
                                             transaction_token=payment["id"], customer=customer)
                order.items.set(item_list)
                serializer = OrderSerializer(order)
                response = {
                    "success": True,
                    "message": "Payment request created succesfully",
                    "order_id": serializer.data["order_id"],
                    "transaction_token": payment["id"],
                    "amount": payment["amount"]
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {"success": False, "message": "Payment request could not be created"}
                return Response(response)
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
        print(serializer.data['store_id'])
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
            order.delivery_status = Order_status[3]
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
def pastOrders(request, userId):
    orders = Order.objects.filter(customer=userId)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def orderPrepared(request, *args, **kwargs):
    order = Order.objects.get(id=kwargs['pk'])

    url = STORES_MICROSERVICE_URL + '/stores/' + str(order.store_id)
    succ, resp = send_request_get(url)
    if not succ:
        raise ValidationError("/stores/<int:pk> : Could not connect to stores microservices")

    resp = resp.json()
    body = {'pickup_address': resp['address'],
            'pickup_location_x': resp['locLongitude'],
            'pickup_location_y': resp['locLatitude'],
            'delivery_address': order.delivery_address,
            'order_id': order.id}
    url = DELIVERY_MICROSERVICE_URL + '/delivery/'
    success, response = send_request_post(url, body)
    if not success:
        raise ValidationError("/delivery : Could not connect to delivery microservices")
    response = response.json()
    print(response)
    return JsonResponse({"msg": "Succesfully created delilvery", "delivery_id": response['delivery_partner']})


@api_view(["GET"])
def ordershistory(request):
    i = 1
    response = {}
    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year
    while i < 9:
        totalorders = 0
        totalcost = 0
        orders = Order.objects.filter(order_time__year=currentYear, order_time__month=currentMonth)
        for order in orders:
            totalorders = totalorders + 1
            totalcost = totalcost + order.cost
        print(currentMonth)
        response[month_code[currentMonth]] = {"total Orders": totalorders, "total_sales": totalcost}
        currentMonth = currentMonth - 1
        if (currentMonth == -1):
            currentMonth = 11
            currentYear = currentYear - 1
        i += 1
    return Response(response)


@api_view(["POST"])
def razorverification(request, *args, **kwargs):
    order = Order.objects.get(id=kwargs['pk'])
    status = request.POST.get('status')
    if status == '0':
        order.delete()
        return JsonResponse({"msg": "Payment Failure Order Could not be placed "})
    else:
        items = order.items
        item_list = []
        for item in items.all():
            item_list.append({'id': item.itemId, 'quantity': item.quantity})
        body = {'item_list': item_list, 'store_id': order.store_id}
        url = STORES_MICROSERVICE_URL + '/updateQuantity/'
        success, response = send_request_post(url, body)
        if not success:
            raise ValidationError("/updateQuantity : Could not connect to stores microservices")
        else:
            order.delivery_status=Order_status[1]
            order.save()
            return JsonResponse({"msg": "Order Has been Placed Successfully "})
