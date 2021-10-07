from ..models import Cart
from django.test import Client
from django.urls import reverse, resolve
from .factories import *
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase, override_settings
from ..views import view_cart, add_to_cart, delete_from_cart, delete_all_from_cart, checkout
import shutil
from clients.tests.factories import ClientFactory, ClientLoggedFactory, ShippingAddressFactory
from store.tests.factories import SizesFactory, ProductFactory
from django.http import SimpleCookie


TEST_DIR = 'test_data'


class TestCartView(TestCase):

  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

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
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_post_no_cart(self):
    url = reverse('add_to_cart')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, add_to_cart)

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

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_post_cart_no_items(self):
    client = ClientFactory()
    self.factory = RequestFactory()
    size_created = SizesFactory()
    size = size_created.pk
    quantity = 1
    cart = CartFactory(client=client)
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
    self.assertEqual(cart.products.count(), 1)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_post_new_item(self):
    client = ClientFactory()
    self.factory = RequestFactory()
    size_created = SizesFactory()
    size = size_created.pk
    quantity = 1
    product = OrderedProductFactory(client=client)
    cart = CartFactory(client=client, products=[product, ])
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
    self.assertEqual(cart.products.count(), 2)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_post_cart_item_in(self):
    client = ClientFactory()
    self.factory = RequestFactory()
    size_created = SizesFactory(quantity=3)
    size = size_created.pk
    quantity = 1
    product = OrderedProductFactory(client=client, quantity=1, product_in_size=size_created)
    cart = CartFactory(client=client, products=[product, ])
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
    self.assertEqual(cart.products.count(), 1)
    self.assertEqual(cart.products.all()[0].quantity, 2)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_add_too_many_products(self):
    client = ClientFactory()
    self.factory = RequestFactory()
    size_created = SizesFactory()
    size = size_created.pk
    quantity = 1
    product = OrderedProductFactory(client=client, quantity=size_created.quantity, product_in_size=size_created)
    cart = CartFactory(client=client, products=[product, ])
    request = self.factory.post('/cart/add',
                                {'size': size,
                                 'quantity': quantity,
                                 'device': client.device})

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    request.COOKIES['device'] = client.device
    response = add_to_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/product/' + str(product.pk) + '/')
    self.assertEqual(cart.products.count(), 1)
    self.assertEqual(cart.products.all()[0].quantity, product.quantity)


class TestDeleteFromCart(TestCase):
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_delete_one(self):
    url = reverse('delete_from_cart')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, delete_from_cart)

    client = ClientFactory()
    size_created = SizesFactory(quantity=3)
    size = size_created.pk
    product = OrderedProductFactory(client=client, quantity=2, product_in_size=size_created)
    cart = CartFactory(client=client, products=[product, ])
    request = self.factory.post('/cart/delete',
                                {'product_in_size': size,
                                 'quantity_delete': 1,
                                 'device': client.device})

    request.COOKIES['device'] = client.device
    response = delete_from_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/')
    self.assertEqual(cart.products.count(), 1)
    self.assertEqual(cart.products.all()[0].quantity, 1)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_delete_more_than_one(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    size_created = SizesFactory(quantity=5)
    size = size_created.pk
    product = OrderedProductFactory(client=client, quantity=4, product_in_size=size_created)
    cart = CartFactory(client=client, products=[product, ])
    request = self.factory.post('/cart/delete',
                                {'product_in_size': size,
                                 'quantity_delete': 3,
                                 'device': client.device})

    request.COOKIES['device'] = client.device
    response = delete_from_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/')
    self.assertEqual(cart.products.count(), 1)
    self.assertEqual(cart.products.all()[0].quantity, 1)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_delete_all(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    size_created = SizesFactory(quantity=4)
    size = size_created.pk
    product = OrderedProductFactory(client=client, quantity=3, product_in_size=size_created)
    cart = CartFactory(client=client, products=[product, ])
    request = self.factory.post('/cart/delete',
                                {'product_in_size': size,
                                 'quantity_delete': 3,
                                 'device': client.device})

    request.COOKIES['device'] = client.device
    response = delete_from_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/')
    self.assertEqual(cart.products.count(), 0)
    self.assertEqual(Cart.objects.count(), 0)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_delete_more_than_exists(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    size_created = SizesFactory(quantity=4)
    size = size_created.pk
    product = OrderedProductFactory(client=client, quantity=5, product_in_size=size_created)
    cart = CartFactory(client=client, products=[product, ])
    request = self.factory.post('/cart/delete',
                                {'product_in_size': size,
                                 'quantity_delete': 6,
                                 'device': client.device})

    request.COOKIES['device'] = client.device
    response = delete_from_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/')
    self.assertEqual(cart.products.count(), 0)
    self.assertEqual(Cart.objects.count(), 0)


class TestDeleteAll(TestCase):
  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_delete_all_existing_cart(self):
    url = reverse('delete_all_from_cart')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, delete_all_from_cart)

    self.factory = RequestFactory()
    client = ClientFactory()
    cart = CartFactory(client=client, products=[])

    request = self.factory.get('/cart/delete_all', device=client.device)

    request.COOKIES['device'] = client.device
    response = delete_all_from_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/')
    self.assertEqual(Cart.objects.count(), 0)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_delete_all_not_existing_cart(self):
    url = reverse('delete_all_from_cart')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, delete_all_from_cart)

    self.factory = RequestFactory()
    client = ClientFactory()

    request = self.factory.get('/cart/delete_all', client=client)

    request.COOKIES['device'] = client.device
    response = delete_all_from_cart(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/products/')
    self.assertEqual(Cart.objects.count(), 0)


class TestCheckout(TestCase):
  def test_no_cart(self):
    url = reverse('checkout')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, checkout)

    client = ClientFactory()
    request = self.factory.get('checkout')

    request.COOKIES['device'] = client.device
    response = checkout(request)
    response.client = Client()

    response.client.cookies = SimpleCookie({'device': client.device})

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/products/')
    self.assertEqual(Cart.objects.count(), 0)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_cart_no_shipping(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    size_created = SizesFactory(quantity=4)
    product = OrderedProductFactory(client=client, quantity=5, product_in_size=size_created)

    cart = CartFactory(client=client, products=[product, ])

    request = self.factory.get('checkout')

    request.COOKIES['device'] = client.device
    response = checkout(request)
    response.client = Client()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Cart.objects.count(), 1)
    self.assertIn('Add shipping address', str(response.content))

  def test_cart_with_shipping(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    size_created = SizesFactory(quantity=4)
    shipping_address = ShippingAddressFactory(client=client)
    product = OrderedProductFactory(client=client, quantity=5, product_in_size=size_created)

    cart = CartFactory(client=client, products=[product, ])

    request = self.factory.get('checkout')

    request.COOKIES['device'] = client.device
    response = checkout(request)
    response.client = Client()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Cart.objects.count(), 1)
    self.assertIn(shipping_address.town, str(response.content))
    self.assertIn(shipping_address.street, str(response.content))
    self.assertIn(shipping_address.firstname, str(response.content))
    self.assertIn(shipping_address.surname, str(response.content))


