from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Cart, OrderedProduct
from django.views.generic import ListView
from store.views import Product, Sizes
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from clients.models import Client, ShippingAddress
from clients.functions import get_client


def view(request):
  client = get_client(request)
  cart, created = Cart.objects.get_or_create(client=client)
  cart.get_total_price()
  cart = Cart.objects.filter(client=client)
  context = {'cart': cart}
  template = 'cart/view.html'
  return render(request, template, context)


def add_quantity(order_item, quantity):
  order_item.quantity += int(quantity)
  order_item.save()


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
  current_cart = Cart.get_cart_by_client(client)[0]

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
    if order_item.quantity == 0:
      order_item.delete()
      if not current_cart.products.exists():
        current_cart.delete()
    return redirect("cart_view")
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
  template = 'cart/checkout.html'
  try:
    shipping_address = ShippingAddress.objects.get(client=client)
    context = {'shipping_address': shipping_address, 'cart': current_cart}
  except:
    context = {'cart': current_cart}
  return render(request, template, context)
