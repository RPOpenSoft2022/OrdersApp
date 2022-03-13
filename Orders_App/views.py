import datetime

from django.shortcuts import render
from django.http import HttpResponse
from Orders_App.models import *
from Orders_App.serializers import OrderSerializer
from rest_framework import generics
import json


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        if self.request.method == "POST":
            item_list = []
            items = json.loads(self.request.POST.get("items"))
            for item in items:
                item_list.append(Item.objects.create(itemId=item["item_id"], quantity=item["quantity"]))
            serializer.save(item_list=item_list, order_time=datetime.time)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
