from django.db import models
from store.models import Product
from django.conf import settings
from django.contrib.auth.models import User


class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  products = models.ManyToManyField(Product, null=True)
  timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
  total_price = models.IntegerField(default=10)

  def __str__(self):
    return "Cart id: %s" % self.id

  def get_total_price(self):
    total = 0
    for order_item in self.products.all():
      total += int(order_item.price)
    return total
