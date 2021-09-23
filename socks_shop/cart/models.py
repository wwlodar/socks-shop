from django.db import models
from store.models import Product, Sizes
from django.conf import settings
from django.contrib.auth.models import User
from clients.models import Client, ShippingAddress


class OrderedProduct(models.Model):
  client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
  ordered = models.BooleanField(default=False)
  product_in_size = models.ForeignKey(Sizes, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=1)

  def get_total_item_price(self):
    return self.quantity * self.product_in_size.price

  def __str__(self):
    return f"{self.product_in_size.product}, {self.product_in_size}, {self.quantity}"


class Cart(models.Model):
  client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
  products = models.ManyToManyField(OrderedProduct)
  timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
  total_price = models.IntegerField(default=10)

  def __str__(self):
    return "Cart id: %s" % self.id

  def get_total_price(self):
    total = 0
    for order_item in self.products.all():
      total += int(order_item.get_total_item_price())
    return total


class Order(models.Model):
  shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
  products = models.ManyToManyField(OrderedProduct)
  date_of_order = models.DateTimeField(auto_now_add=True, auto_now=False)
  total_price = models.IntegerField(default=10)
  paid = models.BooleanField(default=False)
  device = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)