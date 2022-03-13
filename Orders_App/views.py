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

    def get_queryset(self):
        print(self.request.headers['token'])
        return Order.objects.all()

    def perform_create(self, serializer):
        if self.request.method == "POST":
            item_list = []
            items = json.loads(self.request.POST.get("item_list"))
            for item in items:
                item_list.append(Item.objects.create(itemId=item["item_id"], quantity=item["quantity"]))
            serializer.save(items=item_list, order_time=datetime.time)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        item_list = Order.objects.get(pk=self.kwargs['pk']) .items.all()
        if self.request.POST.get("token"):
            serializer.token = self.request.POST.get("token")
        if self.request.POST.get("customer"):
            serializer.customer = self.request.POST.get("customer")
        if self.request.POST.get("transaction_token"):
            serializer.transaction_token = self.request.POST.get("transaction_token")
        if self.request.POST.get("item_list"):
            item_list = []
            items = json.loads(self.request.POST.get("item_list"))
            for item in items:
                item_list.append(Item.objects.create(itemId=item["item_id"], quantity=item["quantity"]))
        serializer.save(items=item_list)
