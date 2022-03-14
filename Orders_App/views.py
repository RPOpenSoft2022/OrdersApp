from rest_framework.exceptions import ValidationError
from Orders_App.models import *
from Orders_App.serializers import OrderSerializer, ReviewSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import datetime


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
        item_list = Order.objects.get(pk=self.kwargs['pk']) .items.all()
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


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        print(self.request.POST)
        order = Order.objects.get(id=self.request.POST.get("order_id"))
        text = self.request.POST.get("review_text")
        score = self.request.POST.get("review_score")
        print(text)
        serializer.save(order=order, text=text, score=score)


@api_view(['POST'])
def review_detail(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST.get("order_id"))
        review = Review.objects.get(order=order)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
