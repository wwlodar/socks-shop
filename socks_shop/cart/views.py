from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Cart, OrderedProduct
from django.views.generic import ListView
from store.views import Product
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


def add_to_cart(request, pk):
  if request.method == 'GET':
    quantity = request.GET.get('quantity')

    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderedProduct.objects.get_or_create(
      product=product,
      user=request.user,
      ordered=False
    )
    current_cart = Cart.objects.filter(user=request.user)

    if current_cart.exists():
      order = current_cart[0]
      if not order.products.filter(product__pk=product.pk).exists():
        order.products.add(order_item)
        order.products.filter(product__pk=product.pk).update(quantity=quantity)
        messages.info(request, "Added New Item")
        return redirect('cart_view')
      else:
        if int(quantity) + int(order.products.filter(product__pk=product.pk).get().quantity) <= int(Product.objects.get(pk=product.pk).quantity):
          order_item.quantity += int(quantity)
          order_item.save()
          messages.info(request, "Added Item")
          return redirect('cart_view')
        else:
          messages.info(request, "You cannot order this quantity of product. "
                                "There are only " + str(Product.objects.get(pk=product.pk).quantity) + " items left and you have "
          + str(order_item.quantity) + " in your cart.")
          return redirect('product_detail', pk=product.pk)

    else:
      timestamp = timezone.now()
      current_cart = Cart.objects.create(user=request.user, timestamp=timestamp)
      current_cart.products.add(order_item)
      current_cart.products.filter(product__pk=product.pk).update(quantity=quantity)
      messages.info(request, "Item added to your cart")
      return redirect('cart_view')


def delete_from_cart(request, pk):
  if request.method == 'GET':
    quantity_delete = request.GET.get('quantity_delete')

    ordered_products = get_object_or_404(OrderedProduct, pk=pk)
    product = ordered_products.product
    current_cart = Cart.objects.filter(user=request.user)

    if current_cart.exists():
      order = current_cart[0]
      if order.products.filter(product__pk=product.pk).exists():
        ordered_products.quantity -= int(quantity_delete)
        ordered_products.save()
        if ordered_products.quantity == 0:
          ordered_products.delete()
        messages.info(request, " Item was removed from your cart")
        return redirect("cart_view")
      return redirect("cart_view")
    else:
      messages.info(request, "This Item not in your cart")
      return redirect("product_detail", pk=pk)


def delete_all_from_cart(request):
  current_cart = Cart.objects.filter(user=request.user)
  if current_cart.exists():
    current_cart.delete()
    messages.info(request, "All items were removed")
    return redirect("cart_view")
  else:
    messages.info(request, "There were no items in your cart")
    return redirect("products_page")
