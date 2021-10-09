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

from rest_framework import serializers


class StatusSerializer(serializers.ModelSerializer):
  pass


def notify_payment_view(request):
  print('get_to_view')
  print(request.method)
  print(request.body)
  if request.method == 'POST':
    logger.debug('POST')
    serializer = StatusSerializer(
      data=json.loads(request.body))

    if not serializer.is_valid():
      logger.exception(u"PayU: Unsupported data. {0}".format(
        force_text(request.body)))
      return HttpResponse('')

    try:
      logger.debug("Fetching order")
      order = Order.objects.get(
        external_id=serializer.validated_data['order']['extOrderId'])
    except Order.DoesNotExist:
      logger.exception(
        u"PayU: order does not exist. {0}".format(
          force_text(request.body)))
      return HttpResponse('')

    if order.status != 'COMPLETED':
      logger.debug("Order.status was not completed yet!")
      with transaction.atomic():
        if serializer.validated_data['order']['status'] == 'COMPLETED':
          logger.debug(f"The concerned order.status {order} is completed: {order.status}")
          order.status = 'COMPLETED'
          order.status_date = datetime.date.today()
          order.save()
        elif serializer.validated_data['order']['status'] == 'PENDING':
          logger.debug("ZWALIDOWANY order.status JEST PENDING")
          pass
        else:
          logger.debug(u"ZWALIDOWANY order.status = {0}".format(serializer.validated_data['order']['status']))
          order.status = 'CANCELED'
          order.status_date = datetime.date.today()
          order.save()
    return HttpResponse('')
