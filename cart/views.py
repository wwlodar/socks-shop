from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Cart, OrderedProduct, Order
from store.views import Product, Sizes
from django.contrib import messages
from clients.models import Client, ShippingAddress
from clients.functions import get_client
from .functions import *
import secrets
import string
from django.contrib.auth.models import User
from .forms import *
from payments.utils import send_payu_order

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
import logging
logger = logging.getLogger(__name__)
def view_cart(request):
  client = get_client(request)
  cart = Cart.objects.filter(client=client)
  if cart.exists():
    cart = Cart.objects.get(client=client)
    cart.get_total_price()
  cart = Cart.objects.filter(client=client)
  context = {'cart': cart}
  template = 'cart/view.html'
  return render(request, template, context)


def add_to_cart(request):
  size = request.POST['size']
  quantity = request.POST['quantity']
  size_chosen = Sizes.objects.get(pk=size)
  client = get_client(request)

  order_item, created = OrderedProduct.objects.get_or_create(
    product_in_size=size_chosen,
    client=client,
    ordered=False
  )
  current_cart, created = Cart.objects.get_or_create(client=client)

  if not Cart.get_product_from_cart(client, size_chosen).exists():
    current_cart.products.add(order_item)
    Cart.get_product_from_cart(client, size_chosen).update(quantity=quantity)
    return redirect('cart_view')
  else:
    if int(quantity) + int(Cart.get_product_from_cart(client, size_chosen).get().quantity) <= int(
        Sizes.objects.get(pk=size_chosen.pk).quantity):
      add_quantity(order_item, quantity)
      return redirect('cart_view')
    else:
      messages.info(request, "You cannot order this quantity of product. There are only "
                    + str(Sizes.objects.get(pk=size_chosen.pk).quantity) +
                    " items left and you have " + str(order_item.quantity) + " in your cart.")
      product = size_chosen.product
      return redirect('product_detail', pk=product.pk)


def delete_from_cart(request):
  quantity = -int(request.POST['quantity_delete'])
  product_in_size = request.POST['product_in_size']
  size_chosen = Sizes.objects.get(pk=product_in_size)

  client = get_client(request)
  order_item = get_object_or_404(OrderedProduct, product_in_size=product_in_size, client=client)
  current_cart = Cart.get_cart_by_client(client)[0]

  if Cart.get_product_from_cart(client, size_chosen).exists():
    add_quantity(order_item, quantity)
    if order_item.quantity <= 0:
      order_item.delete()
      if current_cart.products.count() == 0:
        current_cart.delete()
  return redirect("cart_view")


def delete_all_from_cart(request):
  client = get_client(request)
  current_cart = Cart.get_cart_by_client(client)
  if current_cart.exists():
    current_cart.delete()
    return redirect("cart_view")
  else:
    return redirect("products_page")


def checkout(request):
  client = get_client(request)
  current_cart = Cart.get_cart_by_client(client)
  if not current_cart.exists():
    return redirect('products_page')
  else:
    template = 'cart/checkout.html'
    try:
      shipping_address = ShippingAddress.objects.get(client=client)
      context = {'shipping_address': shipping_address, 'cart': current_cart}
    except:
      context = {'cart': current_cart}
    return render(request, template, context)


def add_email(request):
  client = get_client(request)
  if request.user.is_authenticated:
    return redirect("proceed_to_payment")
  else:
    form = AddEmailForm()
    context = {'form': form}
    template = 'cart/add_email.html'
    return render(request, template, context)


def proceed_to_payment(request):
  client = get_client(request)
  if not request.user.is_authenticated:
    email = request.POST['email']
    password = ""
    for _ in range(9):
      password += secrets.choice(string.ascii_lowercase)
    password += secrets.choice(string.ascii_uppercase)
    password += secrets.choice(string.digits)
    User.objects.create(client=client, email=email, password= password, username=email)
  order = Order.objects.create(client=client)
  cart = Cart.objects.get(client=client)
  order.populate_from_cart(cart=cart)

  url = send_payu_order(request=request)
  print('the returned URL is ', url)

  if url:
    logger.debug(f'Redirecting to {url}')
    print(1)
    return redirect(url)
  else:
    logger.debug(f'No URL returned')
    print(2)
    raise Http404()


from django import http
import sys
from django.template import loader, Context


def this_server_error(request, template_name='cart/nondefault500.html'):
  """
  500 error handler.

  Templates: `500.html`
  Context: sys.exc_info() results
   """
  t = loader.get_template(template_name)  # You need to create a 500.html template.
  ltype, lvalue, ltraceback = sys.exc_info()
  context = {'type': ltype, 'value': lvalue, 'traceback': ltraceback}
  return http.HttpResponseServerError(t.render(context))
