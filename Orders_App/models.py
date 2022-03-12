from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Order(models.Model):
    token = models.CharField(default='', blank=False, max_length=200)
    # "item_list" field is automatically added to each order and can be used to retrieve all items whose foreign-key
    # is this particular Order (Example view and url added as comment)
    order_time = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.CharField(default='', blank=False, max_length=200)
    transaction_token = models.CharField(default='', blank=False, max_length=200)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item_list', null=True, blank=True)
    itemId = models.CharField(default='', blank=False, max_length=200)
    quantity = models.IntegerField(null=True)