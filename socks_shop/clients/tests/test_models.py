from django.test import RequestFactory, TestCase
from django.conf import settings
import factory
from .factories import ClientFactory, ShippingAddressFactory, UserFactory


class TestUser(TestCase):
  def test_factory(self):
    user = UserFactory()

    assert user is not None
    assert user.username != ""


class TestClient(TestCase):
    def test_factory(self):
      client = ClientFactory()

      assert client is not None
      assert client.device != ""


class TestShippingAddress(TestCase):
  def test_factory(self):
    shipping_address = ShippingAddressFactory()

    assert shipping_address is not None
    assert shipping_address.street != ""
    assert shipping_address.town != ""
    assert shipping_address.firstname != ""
    assert shipping_address.surname != ""
    assert shipping_address.client != ""
