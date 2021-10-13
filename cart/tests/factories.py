import factory
from .. import models as models
from clients.tests.factories import ClientFactory
from store.tests.factories import SizesFactory
import random
from factory import fuzzy
import datetime


class OrderedProductFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.OrderedProduct

  client = factory.SubFactory(ClientFactory)
  ordered = False
  product_in_size = factory.SubFactory(SizesFactory)
  quantity = random.randint(1, 20)


class CartFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Cart

  client = factory.SubFactory(ClientFactory)
  timestamp = factory.fuzzy.FuzzyDate(datetime.date(2021, 1, 1))
  total_price = random.randint(1, 20)

  @factory.post_generation
  def products(self, create, extracted, **kwargs):
    if not create:
      # Simple build, do nothing.
      return

    if extracted:
      # A list of groups were passed in, use them
      for product in extracted:
        self.products.add(*extracted)


class OrderFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Order

  street = factory.Faker('street_address')
  town = factory.Faker('city')
  firstname = factory.Faker('first_name')
  surname = factory.Faker('last_name')
  date_of_order = factory.fuzzy.FuzzyDate(datetime.date(2021, 1, 1))
  total_price = random.randint(1, 20)
  client = factory.SubFactory(ClientFactory)
  payment_status = 'NEW'

  @factory.post_generation
  def products(self, create, extracted, **kwargs):
    if not create or not extracted:
      # Simple build, or nothing to add, do nothing.
      return

    # Add the iterable of groups using bulk addition
    self.products.add(*extracted)

