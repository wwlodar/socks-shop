from django.test import RequestFactory, TestCase
from django.conf import settings
import factory
from .. import models as models
from factory import fuzzy
import datetime
import tempfile
from PIL import Image


class HomepagePromotionalFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.HomepagePromotional

  text = 'test'
  image = tempfile.NamedTemporaryFile(suffix=".jpg").name


class CategoryFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Category

  name = 'test'
  date_added = factory.fuzzy.FuzzyDate(datetime.date(2021, 1, 1))


class ProductFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Product

  name = 'test'
  description = 'test'
  image = factory.django.ImageField(color='blue', height=400, width=400)
  category = factory.SubFactory(CategoryFactory)


class SizesFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Sizes

  size_type = factory.fuzzy.FuzzyChoice(models.Sizes.sizes)
  price = factory.Faker('number')
  date_added = factory.fuzzy.FuzzyDate(datetime.date(2021, 1, 1))
  quantity = factory.Faker('number')
  product = factory.SubFactory(ProductFactory)
