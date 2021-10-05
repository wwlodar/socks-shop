from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from ..models import Cart, OrderedProduct
from store.views import Product, Sizes
from django.contrib import messages
from clients.functions import get_client
from django.test import Client
from django.urls import reverse, resolve
from .factories import *
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase, override_settings
from ..views import view_cart, add_quantity, add_to_cart, delete_from_cart, delete_all_from_cart, checkout
from clients.tests.factories import ClientFactory, ClientLoggedFactory, ShippingAddressFactory
from clients.models import Client as ClientModel
import shutil
from clients.tests.factories import ClientFactory, ClientLoggedFactory
from store.tests.factories import SizesFactory, ProductFactory
from django.http import HttpRequest, QueryDict, SimpleCookie

TEST_DIR = 'test_data'


class TestCartView(TestCase):

  def test_cart_view_empty_cart(self):
    url = reverse('cart_view')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, view_cart)

    request = self.factory.get('/cart')
    request.COOKIES['device'] = ClientFactory().device
    response = view_cart(request)
    self.assertEqual(response.status_code, 200)
    self.assertIn("You currently don\\\'t have any items in your cart", str(response.content))

  def test_cart_view_empty_cart_cart_exists(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    cart = CartFactory(client=client)
    request = self.factory.get('/cart', client=client)
    request.COOKIES['device'] = client.device
    response = view_cart(request)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Cart.objects.count(), 1)
    self.assertIn("You currently don\\\'t have any items in your cart", str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_cart_view_cart_exists_one_product(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    ordered_product = OrderedProductFactory(client=client)
    cart = CartFactory(client=client, products=(ordered_product,))
    request = self.factory.get('/cart', client=client)
    request.COOKIES['device'] = client.device
    response = view_cart(request)

    self.assertEqual(response.status_code, 200)
    self.assertIn(str(ordered_product.get_total_item_price()), str(response.content))
    self.assertIn(ordered_product.product_in_size.product.name, str(response.content))
    self.assertIn(str(ordered_product.quantity), str(response.content))
    self.assertIn(ordered_product.product_in_size.product.description, str(response.content))
    self.assertIn(str(ordered_product.product_in_size.price), str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_cart_view_cart_exists_two_products(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    ordered_product1 = OrderedProductFactory(client=client)
    ordered_product2 = OrderedProductFactory(client=client)
    cart = CartFactory(client=client, products=(ordered_product1, ordered_product2))
    request = self.factory.get('/cart', client=client)
    request.COOKIES['device'] = client.device
    response = view_cart(request)
    total_price = str(ordered_product1.get_total_item_price() + ordered_product2.get_total_item_price())

    self.assertEqual(response.status_code, 200)
    self.assertIn(ordered_product1.product_in_size.product.name, str(response.content))
    self.assertIn(str(ordered_product1.quantity), str(response.content))
    self.assertIn(ordered_product1.product_in_size.product.description, str(response.content))
    self.assertIn(str(ordered_product1.product_in_size.price), str(response.content))

    self.assertEqual(response.status_code, 200)
    self.assertIn(ordered_product2.product_in_size.product.name, str(response.content))
    self.assertIn(str(ordered_product2.quantity), str(response.content))
    self.assertIn(ordered_product2.product_in_size.product.description, str(response.content))
    self.assertIn(str(ordered_product2.product_in_size.price), str(response.content))

    self.assertIn(total_price, str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_cart_view_cart_exists_two_clients(self):
    self.factory = RequestFactory()
    client1 = ClientFactory(device='b6aa321a-bbbb-bbbb-aaaa-3c2373e5e5d4')
    client2 = ClientFactory()
    ordered_product1 = OrderedProductFactory(client=client1)
    cart = CartFactory(client=client1, products=(ordered_product1,))
    request = self.factory.get('/cart', client=client2)
    request.COOKIES['device'] = client2.device
    response = view_cart(request)

    self.assertEqual(response.status_code, 200)
    self.assertIn("You currently don\\\'t have any items in your cart", str(response.content))


class TestAddToCart(TestCase):
  def test_post_no_cart(self):
    url = reverse('add_to_cart')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, add_to_cart)

    self.factory = RequestFactory()
    client = ClientFactory()
    size_created = SizesFactory()
    size = size_created.pk
    quantity = 1
    request = self.factory.post('/cart/add',
                                {'size': size,
                                 'quantity': quantity,
                                 'device': client.device})

    request.COOKIES['device'] = client.device
    response = add_to_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/')
    self.assertEqual(Cart.objects.count(), 1)
    cart = Cart.objects.get(client=client)
    self.assertEqual(cart.products.count(), 1)

  def test_post_cart_no_items(self):
    pass

  def test_post_new_item(self):
    pass

  def test_post_cart_item_in(self):
    pass

  def test_add_too_many_products(self):
    pass
