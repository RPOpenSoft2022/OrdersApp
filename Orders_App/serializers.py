from rest_framework import serializers
from Orders_App.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'items', 'order_time', 'customer', 'transaction_token', 'review_text', 'review_score',
                  'delivery_otp', 'delivery_status']

    def to_representation(self, instance):
        item_list = []
        for item in instance.items.all():
            item_list.append({"item_id": item.itemId, "quantity": item.quantity})
        return {
            "order_id": instance.id,
            "item_list": item_list,
            "order_time": instance.order_time,
            "customer": instance.customer,
            "transaction_token": instance.transaction_token,
            "active_status": instance.active_status,
            "review_text": instance.review_text,
            "review_score": instance.review_score,
            "delivery_status": instance.delivery_status,
            "delivery_otp": instance.delivery_otp
        }
