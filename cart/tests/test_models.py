from django.test import TestCase, override_settings
from .factories import *
from ..models import *
from clients.tests.factories import ClientFactory, ClientLoggedFactory, ShippingAddressFactory
from clients.models import Client
import shutil

TEST_DIR = 'test_data'


class TestOrderedProduct(TestCase):
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_factories(self):
    orderedproduct = OrderedProductFactory()

    assert orderedproduct.ordered != ""
    assert orderedproduct.product_in_size != ""
    assert orderedproduct.quantity != ""
    assert orderedproduct.client != ""

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_str(self):
    orderedproduct = OrderedProductFactory()
    self.assertEqual(str(orderedproduct),
                     f"{orderedproduct.product_in_size.product}, {orderedproduct.product_in_size}, {orderedproduct.quantity}")

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_total_item_price(self):
    orderedproduct = OrderedProductFactory()
    price = orderedproduct.quantity * orderedproduct.product_in_size.price
    self.assertEqual(orderedproduct.get_total_item_price(), price)


class TestCart(TestCase):
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_factory(self):
    client = ClientFactory()
    product1 = OrderedProductFactory(client=client)
    product2 = OrderedProductFactory(client=client)
    cart = CartFactory.create(products=(product1, product2), client=client)

    assert cart.timestamp != ""
    assert cart.total_price != ""
    assert cart.client != ""
    self.assertEqual(cart.products.count(), 2)

  def test_empty_cart(self):
    cart = CartFactory.create()

    assert cart.timestamp != ""
    assert cart.total_price != ""
    assert cart.client != ""
    self.assertEqual(cart.products.count(), 0)

  def test_str(self):
    cart = CartFactory.create()
    self.assertEqual(str(cart), "Cart id: %s" % cart.id)

  def test_get_total_price_no_products(self):
    cart = CartFactory.create()
    cart.get_total_price()
    self.assertEqual(cart.total_price, 0)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_total_price_with_products(self):
    product1 = OrderedProductFactory()
    product2 = OrderedProductFactory()
    cart = CartFactory.create(products=(product1, product2))
    cart.get_total_price()
    self.assertNotEqual(cart.total_price, 0)

  def test_get_cart_by_client(self):
    client = ClientFactory()
    cart = CartFactory.create(client=client)
    print(Cart.get_cart_by_client(client))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_product_from_cart(self):
    client = ClientFactory()
    product = OrderedProductFactory()
    cart = CartFactory.create(client=client, products=(product,))
    print(Cart.get_product_from_cart(client, size_chosen=product.product_in_size))


class TestOrder(TestCase):
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_factory(self):
    client = ClientFactory()
    product1 = OrderedProductFactory(client=client)
    product2 = OrderedProductFactory(client=client)
    order = OrderFactory.create(products=(product1, product2), client=client)

    assert order is not None
    assert order.street != ""
    assert order.town != ""
    assert order.firstname != ""
    assert order.surname != ""
    assert order.products != ""
    assert order.date_of_order != ""
    assert order.total_price != ""
    assert order.paid != ""
    assert order.client != ""

    self.assertEqual(Order.objects.count(), 1)
    self.assertEqual(Client.objects.count(), 1)
    self.assertEqual(order.products.count(), 2)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_method(self):
    client = ClientFactory()
    shipping_address = ShippingAddressFactory(client=client)
    product1 = OrderedProductFactory(client=client)
    product2 = OrderedProductFactory(client=client)
    cart = CartFactory.create(products=(product1, product2), client=client)
    order = OrderFactory(client=client)

    order = order.populate_from_cart(cart=cart)
    self.assertEqual(order.client, client)
    self.assertEqual(order.client, cart.client)
    self.assertEqual(order.street, cart.client.shippingaddress.street)
    self.assertEqual(order.town, cart.client.shippingaddress.town)
    self.assertEqual(order.firstname, cart.client.shippingaddress.firstname)
    self.assertEqual(order.surname, cart.client.shippingaddress.surname)
    self.assertEqual(order.total_price, cart.total_price)
    self.assertEqual(cart.products.all()[0], order.products.all()[0])
    self.assertEqual(cart.products.all()[1], order.products.all()[1])

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_street(self):
    street = 'dummy_street 1'
    order = OrderFactory(street=street)

    self.assertEqual(order.street, street)

  def test_town(self):
    town = 'dummy_town'
    order = OrderFactory(town=town)

    self.assertEqual(order.town, town)

  def test_firstname(self):
    firstname = 'dummy_firstname'
    order = OrderFactory(firstname=firstname)

    self.assertEqual(order.firstname, firstname)

  def test_surname(self):
    surname = 'dummy_surname'
    order = OrderFactory(surname=surname)

    self.assertEqual(order.surname, surname)

  def test_client(self):
    client = ClientFactory()
    order = OrderFactory(client=client)

    self.assertEqual(order.client, client)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_product(self):
    product = OrderedProductFactory()
    order = OrderFactory(products=(product,))

    self.assertEqual(order.products.all()[0], product)
    self.assertEqual(order.products.count(), 1)

  def test_total_price(self):
    total_price = 80
    order = OrderFactory(total_price=total_price)

    self.assertEqual(order.total_price, total_price)
