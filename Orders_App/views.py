from django.shortcuts import render
from django.http import HttpResponse
from Orders_App.models import *

"""
# Example on how to retrieve orders and their item lists
def example_item_list(request):
    orders = Order.objects.all()
    out = ""
    for order in orders:
        out += "Order token - " + order.token + "</br>Item List - ["
        for item in order.item_list.all():
            out += "(id: " + item.itemId + ", quantity: " + str(item.quantity) + "), "
    out += "]</br></br>"
    return HttpResponse(out)
"""
