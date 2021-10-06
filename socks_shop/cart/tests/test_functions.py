from ..functions import *
from .factories import *

from django.test import override_settings, TestCase
import shutil

TEST_DIR = 'test_data'


class TestAddQuantity(TestCase):
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_add_one(self):
    order_item = OrderedProductFactory(quantity=1)
    add_quantity(order_item, 1)
    self.assertEqual(order_item.quantity, 2)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_add_more_than_one(self):
    order_item = OrderedProductFactory(quantity=2)
    add_quantity(order_item, 2)
    self.assertEqual(order_item.quantity, 4)
