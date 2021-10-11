from django.shortcuts import render
from clients.functions import *
from cart.models import Order
from .utils import *
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.urls import reverse
from datetime import datetime
from .utils import send_payu_order


@csrf_exempt
def notify_payment_view(request):
  if request.method == 'POST':
    print('POST')
    data = json.loads(request.body)
    order_id = (data['order']['extOrderId'])
    print("Fetching order")
    order = Order.objects.get(pk=order_id)

    if order.payment_status != 'COMPLETED':
      print(f"{order} was not completed yet!")
      with transaction.atomic():
        if data['order']['status'] == 'COMPLETED':
          print(f"The concerned {order} is completed: {order.payment_status}")
          order.payment_status = 'COMPLETED'
          order.status_date = datetime.today()
          order.save()
        elif data['order']['status'] == 'PENDING':
          print(f"{order} JEST PENDING")
          pass
        else:
          print(u"order.payment_status = {0}".format(data['order']['status']))
          order.payment_status = 'CANCELED'
          order.status_date = datetime.today()
          order.save()
    return HttpResponse('')


def after_payment(request):
  client = get_client(request)
  order = Order.objects.filter(client=client).order_by('-date_of_order')[0]
  order_id = order.pk
  return render(request, 'payments/after_payment.html', {'order_id': order_id})
