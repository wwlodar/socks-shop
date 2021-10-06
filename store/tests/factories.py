import factory
from .. import models as models
from factory import fuzzy
import datetime
import tempfile
import random


class HomepagePromotionalFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.HomepagePromotional

  text = 'test_text'
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
  category = factory.SubFactory(CategoryFactory)
  image = factory.django.ImageField(color='blue', height=400, width=400)


class SizesFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.Sizes

  size_type = factory.fuzzy.FuzzyChoice(models.Sizes.sizes)
  price = random.randint(1, 20)
  date_added = factory.fuzzy.FuzzyDate(datetime.date(2021, 1, 1))
  quantity = random.randint(1, 20)
  product = factory.SubFactory(ProductFactory)
