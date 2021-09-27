from django.test import RequestFactory, TestCase
from django.conf import settings
from .factories import *
from django.test import override_settings
import shutil

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

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_size(self):
    product = ProductFactory()
    self.assertEqual(product.image.height, 300)
    self.assertEqual(product.image.width, 300)
