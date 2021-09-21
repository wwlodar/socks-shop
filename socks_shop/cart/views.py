from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Cart, OrderedProduct
from django.views.generic import ListView
from store.views import Product, Sizes
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages


def view(request):
  cart = Cart.objects.filter(user=request.user)
  if cart.exists():
    amount = Cart.objects.get(user=request.user).get_total_price()
    context = {'cart': cart, 'amount': amount}
    template = 'cart/view.html'
    return render(request, template, context)
  context = {'cart': cart}
  template = 'cart/view.html'
  return render(request, template, context)


def add_to_cart(request):
  size = request.POST['size']
  quantity = request.POST['quantity']
  size_chosen = Sizes.objects.get(pk=size)

  order_item, created = OrderedProduct.objects.get_or_create(
    product_in_size=size_chosen,
    user=request.user,
    ordered=False
  )
  current_cart = Cart.objects.filter(user=request.user)
  if current_cart.exists():
    order = current_cart[0]
    if not order.products.filter(product_in_size__pk=size_chosen.pk).exists():
      order.products.add(order_item)
      order.products.filter(product_in_size__pk=size_chosen.pk).update(quantity=quantity)
      return redirect('cart_view')
    else:
      if int(quantity) + int(order.products.filter(product_in_size__pk=size_chosen.pk).get().quantity) <= int(
        Sizes.objects.get(pk=size_chosen.pk).quantity):
        order_item.quantity += int(quantity)
        order_item.save()
        return redirect('cart_view')
      else:
        messages.info(request, "You cannot order this quantity of product. "
                               "There are only " + str(
                      Sizes.objects.get(pk=size_chosen.pk).quantity) +
                      " items left and you have "
                      + str(order_item.quantity) + " in your cart.")
        product = size_chosen.product
        return redirect('product_detail', pk=product.pk)

  else:
    timestamp = timezone.now()
    current_cart = Cart.objects.create(user=request.user, timestamp=timestamp)
    current_cart.products.add(order_item)
    current_cart.products.filter(product_in_size__pk=size_chosen.pk).update(quantity=quantity)
    return redirect('cart_view')


def delete_from_cart(request):
  quantity_delete = request.POST['quantity_delete']
  product_in_size = request.POST['product_in_size']
  size_chosen = Sizes.objects.get(pk=product_in_size)
  ordered_products = get_object_or_404(OrderedProduct, product_in_size=product_in_size)
  current_cart = Cart.objects.filter(user=request.user)

  if current_cart.exists():
    order = current_cart[0]
    if order.products.filter(product_in_size__pk=size_chosen.pk).exists():
      ordered_products.quantity -= int(quantity_delete)
      ordered_products.save()
      if ordered_products.quantity == 0:
        ordered_products.delete()
        if not order.products.exists():
          order.delete()
      return redirect("cart_view")
    return redirect("cart_view")
  else:
    messages.info(request, "This Item not in your cart")
    product = size_chosen.product
    return redirect("product_detail", pk=product.pk)


def delete_all_from_cart(request):
  current_cart = Cart.objects.filter(user=request.user)
  if current_cart.exists():
    current_cart.delete()
    return redirect("cart_view")
  else:
    messages.info(request, "There were no items in your cart")
    return redirect("products_page")
