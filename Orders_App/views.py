from django.shortcuts import render
from django.http import HttpResponse
from Orders_App.models import *
from Orders_App.serializers import OrderSerializer
from rest_framework import generics


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
