from ..models import Cart
from django.test import Client
from django.urls import reverse, resolve
from .factories import *
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase, override_settings
from ..views import view_cart, add_to_cart, delete_from_cart, delete_all_from_cart, checkout, \
  add_email, proceed_to_payment
import shutil
from clients.tests.factories import ClientFactory, ClientLoggedFactory, \
  UserFactory, ShippingAddressFactory
from store.tests.factories import SizesFactory, ProductFactory
from django.http import SimpleCookie
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
import mock

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
    self.assertIn('Add\\n        shipping address', str(response.content))

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


class TestAddEmail(TestCase):

  def test_logged_user(self):
    self.factory = RequestFactory()
    client_logged = ClientLoggedFactory()
    request = self.factory.get('add_email')

    request.user = client_logged.user
    response = add_email(request)
    response.client = Client()
    response.client.force_login(client_logged.user)

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/proceed_to_payment', fetch_redirect_response=False)

  def test_not_logged_user_get(self):
    self.factory = RequestFactory()
    client_not_logged = ClientFactory()
    request = self.factory.get('add_email')

    request.COOKIES['device'] = client_not_logged.device
    request.user = AnonymousUser()
    response = add_email(request)
    response.client = Client()
    print(response)
    self.assertEqual(response.status_code, 200)

  def test_not_logged_user_post_already_in_database(self):
    self.factory = RequestFactory()
    client_not_logged = ClientLoggedFactory()
    email = client_not_logged.user.email
    request = self.factory.post('add_email', {'email': email})

    request.COOKIES['device'] = client_not_logged.device
    request.user = AnonymousUser()
    response = add_email(request)
    response.client = Client()
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/login/')

  def test_not_logged_user_not_in_database(self):
    self.factory = RequestFactory()
    client_not_logged = ClientFactory()
    request = self.factory.post('add_email', {'email': 'test_email@google.com'})

    request.COOKIES['device'] = client_not_logged.device
    request.user = AnonymousUser()
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    response = add_email(request)
    response.client = Client()
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/proceed_to_payment', fetch_redirect_response=False)


class TestProceedToPayment(TestCase):

  @mock.patch('cart.views.send_payu_order', return_value=
  (
      'https://merch-prod.snd.payu.com/pay/?orderId=JSK5KJMMNS211012GUEST000P01&token=eyJhbGciOiJIUzI1NiJ9.eyJvcmRlcklk'
      'IjoiSlNLNUtKTU1OUzIxMTAxMkdVRVNUMDAwUDAxIiwicG9zSWQiOiJiM3dBYzBGZCIsImF1dGhvcml0aWVzIjpbIlJPTEVfQ0xJRU5UIl0sInBh'
      'eWVyRW1haWwiOiJ3ZXJ3bG9kYXJjenlrQHdwLnBsIiwiZXhwIjoxNjM0MTMwMTg2LCJpc3MiOiJQQVlVIiwiYXVkIjoiYXBpLWdhdGV3YXkiLCJ'
      'zdWIiOiJQYXlVIHN1YmplY3QiLCJqdGkiOiI1NDBhMWZhMi1jMTM3LTRkYjItODAyMC1iN2I3NTY1MmJkZmQifQ.0-XasyFCYoU5RZbhgo7jwoH'
      '4gyewjrDmaZGjii3IA8E'
  ))
  def test_proceed_to_payment_url(self, mock_value):
    self.factory = RequestFactory()
    client_not_logged = ClientFactory()
    cart = CartFactory(client=client_not_logged)
    shipping_address = ShippingAddressFactory(client=client_not_logged)
    request = self.factory.get('proceed_to_payment')
    request.COOKIES['device'] = client_not_logged.device

    response = proceed_to_payment(request)
    response.client = Client()
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response,
                         'https://merch-prod.snd.payu.com/pay/?orderId=JSK5KJMMNS211012GUEST000P01&token=eyJhbGciOiJIUz'
                         'I1NiJ9.eyJvcmRlcklkIjoiSlNLNUtKTU1OUzIxMTAxMkdVRVNUMDAwUDAxIiwicG9zSWQiOiJiM3dBYzBGZCIsImF1dG'
                         'hvcml0aWVzIjpbIlJPTEVfQ0xJRU5UIl0sInBheWVyRW1haWwiOiJ3ZXJ3bG9kYXJjenlrQHdwLnBsIiwiZXhwIjoxNjM'
                         '0MTMwMTg2LCJpc3MiOiJQQVlVIiwiYXVkIjoiYXBpLWdhdGV3YXkiLCJzdWIiOiJQYXlVIHN1YmplY3QiLCJqdGkiOiI1'
                         'NDBhMWZhMi1jMTM3LTRkYjItODAyMC1iN2I3NTY1MmJkZmQifQ.0-XasyFCYoU5RZbhgo7jwoH4gyewjrDmaZGjii3IA8E',
                         fetch_redirect_response=False)

  @mock.patch('cart.views.send_payu_order', return_value='')
  def test_proceed_to_payment_Http404(self, mock_value):
    with self.assertRaises(Exception):
      self.factory = RequestFactory()
      client_not_logged = ClientFactory()
      cart = CartFactory(client=client_not_logged)
      shipping_address = ShippingAddressFactory(client=client_not_logged)
      request = self.factory.get('proceed_to_payment')
      request.COOKIES['device'] = client_not_logged.device

      response = proceed_to_payment(request)
      response.client = Client()
