from django.test import RequestFactory, TestCase
from django.conf import settings
import factory
from .. import models as models


class HomepagePromotionalFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.HomepagePromotional

  text = 'test'
  image = 'test'


class CategoryFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.HomepagePromotional

  name = 'test'
  date_added = 'test'


class ProductFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.HomepagePromotional

  name = 'test'
  description = 'test'
  image = ''
  category = factory.SubFactory(CategoryFactory)


class SizesFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.HomepagePromotional

  size_type = 'test'
  price = ''
  date_added = ''
  quantity = ''
  product = factory.SubFactory(ProductFactory)
