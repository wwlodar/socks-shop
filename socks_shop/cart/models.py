from django.db import models
from store.models import Product
from django.conf import settings
from django.contrib.auth.models import User


class OrderedProduct(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  ordered = models.BooleanField(default=False)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)

  def get_total_item_price(self):
    return self.quantity * self.product.price


class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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
