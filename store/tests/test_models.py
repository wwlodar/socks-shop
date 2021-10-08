from django.test import RequestFactory, TestCase
from django.conf import settings
from .factories import *
from django.test import override_settings
import shutil
from ..models import Sizes, Product

TEST_DIR = 'test_data'


class TestHomepagePromotional(TestCase):
  def test_factory(self):
    homepage = HomepagePromotionalFactory()

    assert homepage is not None
    assert homepage.text != ""
    assert homepage.image != ""


class TestCategory(TestCase):
  def test_factory(self):
    category = CategoryFactory()

    assert category is not None
    assert category.name != ""
    assert category.date_added != ""

  def test_str(self):
    category = CategoryFactory()
    self.assertEqual(str(category), category.name)


class TestProduct(TestCase):
  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def setUp(self):
    self.product = ProductFactory()

  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  def test_factory(self):
    assert self.product is not None
    assert self.product.name != ""
    assert self.product.description != ""
    assert self.product.image != ""
    assert self.product.category != ""

  def test_str(self):
    self.assertEqual(str(self.product), f" {str(self.product.name)}")


class TestSize(TestCase):
  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def setUp(self):
    self.sizes = SizesFactory()

  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  def test_factory(self):

    assert self.sizes is not None
    assert self.sizes.size_type != ""
    assert self.sizes.price != ""
    assert self.sizes.date_added != ""
    assert self.sizes.quantity != ""
    assert self.sizes.product != ""

  def test_str(self):
    self.assertEqual(str(self.sizes), f" {str(self.sizes.size_type)}")

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_unique(self):
    product = ProductFactory()
    sizes = Sizes.objects.create(size_type='sm', product=product, price=2, quantity=1)
    self.assertNotEquals(sizes, None)
    with self.assertRaises(Exception):
      Sizes.objects.create(size_type='sm', product=product, price=2, quantity=1)
