from rest_framework.exceptions import ValidationError
from Orders_App.models import *
from django.views.decorators.csrf import csrf_exempt
from Orders_App.serializers import OrderSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
import json
import datetime


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
        item_list = []
        items = json.loads(self.request.POST.get("item_list"))
        for item in items:
            item_list.append(Item.objects.create(itemId=item["item"], quantity=item["quantity"]))
        serializer.save(items=item_list, order_time=datetime.time)


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
        order.active_status = False
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class ReviewDetails(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        review_text = request.POST.get('review_text')
        review_score = request.POST.get('review_score')
        ID = order.id
        return Response({
            'order_id': ID,
            'review_text': review_text,
            'review_score': review_score
        })

    def update(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.review_text = request.POST.get('review_text')
        order.review_score = request.POST.get('review_score')
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

