from ..forms import AddSizeForm
from .factories import *
from django.test import override_settings
import shutil
from ..models import Sizes
from django.test import RequestFactory, TestCase

TEST_DIR = 'test_data'


class TestForms(TestCase):
  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_init(self):
    size = SizesFactory()
    AddSizeForm(pk=size.product.pk)

  def test_init_without_pk(self):
    with self.assertRaises(Exception):
      AddSizeForm()

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_invalid_form(self):
    # form is invalid and unbound
    # as quantity gets populated from js
    product = ProductFactory()
    size1 = SizesFactory(product=product, size_type="EU 35-37")
    form = AddSizeForm(pk=product.pk, data={'quantity': 1, 'size': ''})

    self.assertFalse(form.is_valid())
