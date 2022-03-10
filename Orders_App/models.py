from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Orders(models.Model):
    token = models.CharField(default='', blank=False, max_length=200)
    order_time = models.DateTimeField(auto_now_add=True, blank=True)
    customer = models.CharField(default='', blank=False, max_length=200)
    transaction_token = models.CharField(default='', blank=False, max_length=200)


class Items(models.Model):
    itemId = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='item_list', null=True, blank=True)
    quantity = models.IntegerField(null=True)