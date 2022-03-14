from rest_framework import serializers
from Orders_App.models import Order, Review


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'items', 'order_time', 'customer', 'transaction_token']

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
            "active_status": instance.active_status
        }


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order', 'text', 'score']

    def to_representation(self, instance):
        return {
            "review_id": instance.id,
            "order_id": instance.order.id,
            "review_score": instance.score,
            "review_text": instance.text,
        }