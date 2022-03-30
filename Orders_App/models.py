from django.db import models

Order_status = (
    ('PENDING', 'Payment Pending'),
    ('ACCEPTED', 'Preparing Item'),
    ('OUT_FOR_DELIVERY', 'Out for Delivery'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
)


class Order(models.Model):
    order_time = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.CharField(default='', blank=False, max_length=200)
    customer_name = models.CharField(max_length=400, blank=True)
    customer_phone_no = models.BigIntegerField(blank=True)
    transaction_token = models.CharField(default='', blank=False, max_length=200)
    store_id = models.BigIntegerField(blank=False, null=False)
    store_name = models.CharField(max_length=50, blank=True)
    review_text = models.CharField(max_length=400, blank=True, null=True)
    review_score = models.IntegerField(null=True, blank=True)
    delivery_phone_no = models.BigIntegerField(blank=True)
    delivery_otp = models.IntegerField(null=True, blank=True)
    delivery_status = models.CharField(null=False, blank=False, choices=Order_status, default=Order_status[0],max_length=200)
    delivery_address = models.TextField(blank=True)
    cost = models.IntegerField(null=True, blank=False)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    itemId = models.CharField(default='', blank=False, max_length=200)
    name = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True)
    item_price = models.IntegerField(null=True, blank=True)
