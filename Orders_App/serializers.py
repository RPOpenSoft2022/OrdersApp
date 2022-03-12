from rest_framework import serializers
from Orders_App.models import Order, Item


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'token', 'item_list', 'order_time', 'customer', 'transaction_token']

