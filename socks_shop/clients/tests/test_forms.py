from ..forms import UserRegisterForm, ShippingAddressForm
from .factories import *


class TestForms(TestCase):

  def test_user_register_form_valid_data(self):
    form = UserRegisterForm(data={
      'username': 'test_user',
      'email': 'email@email.com',
      'password1': 'Password1299',
      'password2': 'Password1299'
    })

    self.assertTrue(form.is_valid(), True)

  def test_user_register_form_invalid_data(self):
    form = UserRegisterForm(data={
      'username': 'test_user',
      'email': 'email',
      'password1': 'Password1299',
      'password2': 'Password1299'
    })

    self.assertFalse(form.is_valid(), False)
    self.assertEqual(form.errors, {'email': ['Enter a valid email address.']})

  def test_shipping_address_form_valid_data(self):
    form = ShippingAddressForm(data={
      'street': 'dummy_street',
      'town': 'dummy_town',
      'firstname': 'dummy_firstname',
      'surname': 'dummy_surname',
      'client': ClientFactory()
    })

    self.assertTrue(form.is_valid(), True)

  def test_shipping_address_form_invalid_data(self):
    form = ShippingAddressForm(data={
      'street': 'dummy_street',
      'town': '',
      'firstname': 'dummy_firstname',
      'surname': 'dummy_surname',
      'client': ClientFactory()
    })

    self.assertFalse(form.is_valid(), False)
    self.assertEqual(form.errors, {'town': ['This field is required.']})
