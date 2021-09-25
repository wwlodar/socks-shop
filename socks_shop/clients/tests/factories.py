from django.test import RequestFactory, TestCase
from django.conf import settings
import factory
from .. import models as models


class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = settings.AUTH_USER_MODEL
  username = 'test_user'
  password = factory.PostGenerationMethodCall("set_password", "password")


class ClientFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Client

  device = 'b6aa321a-aaaa-aaaa-aaaa-3c2373e5e5d4'


class ShippingAddressFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.ShippingAddress

  street = factory.Faker('street_address')
  town = factory.Faker('city')
  firstname = factory.Faker('first_name')
  surname = factory.Faker('last_name')
  client = factory.SubFactory(ClientFactory)
