from django.db import models


class Order(models.Model):
    token = models.CharField(default='', blank=False, max_length=200)
    order_time = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.CharField(default='', blank=False, max_length=200)
    transaction_token = models.CharField(default='', blank=False, max_length=200)
    active_status = models.BooleanField(default=True)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    itemId = models.CharField(default='', blank=False, max_length=200)
    quantity = models.IntegerField(null=True)


class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=400)
    score = models.IntegerField(null=True)