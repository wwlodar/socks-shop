from django.shortcuts import render
from clients.functions import *
from cart.models import Order
from .utils import *
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.urls import reverse
from datetime import datetime
from .utils import send_payu_order
import io
from rest_framework.parsers import JSONParser

from rest_framework import serializers


class StatusSerializer(serializers.ModelSerializer):
  pass


@csrf_exempt
def notify_payment_view(request):
  if request.method == 'POST':
    print('POST')
    data = json.loads(request.body)
    order_id = (data['order']['extOrderId'])
    print("Fetching order")
    order = Order.objects.get(pk=order_id)
    print(order)
    print(order.payment_status)

    if order.payment_status != 'COMPLETED':
      print("Order.payment_status was not completed yet!")
      with transaction.atomic():
        if data['order']['status'] == 'COMPLETED':
          print(f"The concerned {order} is completed: {order.payment_status}")
          order.payment_status = 'COMPLETED'
          print(order.payment_status)
          order.status_date = datetime.date.today()
          order.save()
          print(order.payment_status)
        elif data['order']['status'] == 'PENDING':
          print("{order} JEST PENDING")
          pass
        else:
          print(u"ZWALIDOWANY order.payment_status = {0}".format(data['order']['status']))
          order.payment_status = 'CANCELED'
          order.status_date = datetime.date.today()
          order.save()
    return HttpResponse('')


def after_payment(request):
  print(request)
  order_id = request.body
  return render(request, 'payments/after_payment.html', {'order_id': order_id})
