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
  print('get_to_view')
  print(request.method)
  print(request.body)
  print(serializers.Serializer(request.body))
  if request.method == 'POST':
    print('POST')
    data = json.loads(request.body)
    print(data)
    order_id = (data['order']['extOrderId'])
    print("Fetching order")
    print(Order.objects.get(pk=order_id))
    order = Order.objects.get(pk=order_id)
    print(order)
    print(order.status)

  if order.status != 'COMPLETED':
    print("Order.status was not completed yet!")
    with transaction.atomic():
      if data['order']['status'] == 'COMPLETED':
        print(f"The concerned order.status {order} is completed: {order.status}")
        order.status = 'COMPLETED'
        order.status_date = datetime.date.today()
        order.save()
      elif data['order']['status'] == 'PENDING':
        print("ZWALIDOWANY order.status JEST PENDING")
        pass
      else:
        print(u"ZWALIDOWANY order.status = {0}".format(data['order']['status']))
        order.status = 'CANCELED'
        order.status_date = datetime.date.today()
        order.save()
  return HttpResponse('')


def after_payment(request):
  print(request.body)
  print(request.content)
