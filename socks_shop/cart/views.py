from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Cart
from django.views.generic import ListView
from store.views import Product
from django.urls import reverse


def view(request):
  cart = Cart.objects.filter(user=request.user)
  amount = Cart.objects.get(user=request.user).get_total_price()
  context = {'cart': cart, 'amount': amount}
  template = 'cart/view.html'
  return render(request, template, context)


def add_to_cart(request):
  cart = Cart.objects.all()
  try:
    product = Product.objects.get(id=id)
  except Product.DoesNotExist:
    pass
  except:
    pass
  if product not in cart.products.all():
    cart.products.add(product)
  else:
    cart.products.remove(product)
  return redirect(reverse("cart"))
