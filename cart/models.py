from django.db import models
from store.models import Sizes
from clients.models import Client, ShippingAddress


class OrderedProduct(models.Model):
  client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
  ordered = models.BooleanField(default=False)
  product_in_size = models.ForeignKey(Sizes, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=1)

  def get_total_item_price(self):
    return int(self.quantity) * self.product_in_size.price

  def __str__(self):
    return f"{self.product_in_size.product}, {self.product_in_size}, {self.quantity}"


class Cart(models.Model):
  client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
  products = models.ManyToManyField(OrderedProduct)
  timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
  total_price = models.IntegerField(default=0)

  def __str__(self):
    return "Cart id: %s" % self.id

  def get_total_price(self):
    total = 0
    for order_item in self.products.all():
      total += int(order_item.get_total_item_price())
    self.total_price = total
    self.save()

  def get_cart_by_client(client):
    return Cart.objects.filter(client=client).order_by('-timestamp')

  def get_product_from_cart(client, size_chosen):
    return Cart.objects.get(client=client).products.filter(product_in_size__pk=size_chosen.pk)


PAYMENT_STATUS = (
  ('NEW', 'NEW'),
  ('PENDING', 'PENDING'),
  ('CANCELED', 'CANCELED'),
  ('COMPLETED', 'COMPLETED'),
)


class Order(models.Model):
  street = models.CharField(max_length=200, null=False, blank=False)
  town = models.CharField(max_length=200, null=False, blank=False)
  firstname = models.CharField(max_length=200, null=False, blank=False)
  surname = models.CharField(max_length=200, null=False, blank=False)
  products = models.ManyToManyField(OrderedProduct)
  date_of_order = models.DateTimeField(auto_now_add=True, auto_now=False)
  total_price = models.IntegerField(default=10)
  client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
  payment_status = models.CharField(choices=PAYMENT_STATUS, default='NEW', max_length=9)
  status_date = models.DateField(blank=True, null=True, default=None)

  def populate_from_cart(self, cart):
    self.total_price = cart.total_price

    self.client = cart.client
    self.street = cart.client.shippingaddress.street
    self.town = cart.client.shippingaddress.town
    self.firstname = cart.client.shippingaddress.firstname
    self.surname = cart.client.shippingaddress.surname
    for val in cart.products.all():
      self.products.add(val)
    self.save()

    return self
