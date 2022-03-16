from django.db import models

Order_status = (
    ('PENDING', 'Order Pending'),
    ('ACCEPTED', 'Preparing Item'),
    ('OUT_FOR_DELIVERY', 'Out for Delivery'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
)


class Order(models.Model):
    order_time = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.CharField(default='', blank=False, max_length=200)
    transaction_token = models.CharField(default='', blank=False, max_length=200)
    store_id = models.BigIntegerField(blank=False, null=False)
    review_text = models.CharField(max_length=400, blank=True, null=True)
    review_score = models.IntegerField(null=True, blank=True)
    delivery_otp = models.IntegerField(null=True, blank=True)
    delivery_status = models.CharField(null=False, blank=False, choices=Order_status, default=Order_status[0],max_length=200)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    itemId = models.CharField(default='', blank=False, max_length=200)
    quantity = models.IntegerField(null=True)
