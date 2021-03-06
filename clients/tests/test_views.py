from ..views import register, client_profile, add_shipping, change_shipping
from django.test import Client, RequestFactory
from django.urls import reverse, resolve
from .factories import *
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase
from .factories import ClientFactory, ShippingAddressFactory, UserFactory, ClientLoggedFactory
from ..models import ShippingAddress


class TestRegister(TestCase):

  def test_register_get(self):
    url = reverse('register')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, register)

    request = self.factory.get('/register')
    request.COOKIES['device'] = ClientFactory().device
    response = register(request)
    self.assertEqual(response.status_code, 200)

  def test_register_post_success(self):
    self.factory = RequestFactory()
    request = self.factory.post(reverse('register'), {
      'username': 'dummy_username',
      'email': 'email@email.com',
      'password1': 'user.password',
      'password2': 'user.password'})
    request.COOKIES['device'] = ClientFactory().device

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register(request)
    response.client = Client()

    self.assertEqual(response.status_code, 302)
    self.assertEqual(User.objects.count(), 1)
    self.assertRedirects(response, '/login/')

  def test_register_post_failed(self):
    self.factory = RequestFactory()
    request = self.factory.post(reverse('register'), {
      'username': '',
      'email': 'email@email.com',
      'password1': 'password',
      'password2': 'password'})
    request.COOKIES['device'] = ClientFactory().device

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register(request)
    response.client = Client()

    self.assertEqual(User.objects.count(), 0)
    self.assertEqual(response.status_code, 200)


class TestProfile(TestCase):
  def test_unauthenticated_access(self):
    response = self.client.get(reverse('profile'))
    self.assertRedirects(response, '/login/?next=/profile/')

  def test_profile_get(self):
    url = reverse('profile')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, client_profile)

    request = self.factory.get('profile')
    user = UserFactory()
    request.user = user
    response = client_profile(request)
    self.assertEqual(response.status_code, 200)


class TestAddShippingAddress(TestCase):

  def test_add_shipping_get(self):
    url = reverse('add_shipping_address')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, add_shipping)

    request = self.factory.get('/add_shipping_address')
    request.COOKIES['device'] = ClientFactory().device
    response = add_shipping(request)
    self.assertEqual(response.status_code, 200)

  def test_add_shipping_post_success_not_logged(self):
    self.factory = RequestFactory()
    client_chosen = ClientFactory()
    request = self.factory.post(reverse('register'), {
      'street': ShippingAddressFactory.street,
      'town': ShippingAddressFactory.town,
      'firstname': ShippingAddressFactory.firstname,
      'surname': ShippingAddressFactory.surname,
      'client': client_chosen})
    request.COOKIES['device'] = client_chosen.device

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = add_shipping(request)
    response.client = Client()

    self.assertEqual(response.status_code, 302)
    self.assertEqual(ShippingAddress.objects.count(), 1)
    self.assertRedirects(response, '/')

  def test_add_shipping_post_success_logged(self):
    self.factory = RequestFactory()
    client_chosen = ClientLoggedFactory()
    request = self.factory.post(reverse('register'), {
      'street': ShippingAddressFactory.street,
      'town': ShippingAddressFactory.town,
      'firstname': ShippingAddressFactory.firstname,
      'surname': ShippingAddressFactory.surname,
      'client': client_chosen})

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    request.user = client_chosen.user
    response = add_shipping(request)
    response.client = Client()

    self.assertEqual(response.status_code, 302)
    self.assertEqual(ShippingAddress.objects.count(), 1)
    self.assertRedirects(response, '/')

  def test_add_shipping_post_failed(self):
    self.factory = RequestFactory()
    client_chosen = ClientLoggedFactory()
    request = self.factory.post(reverse('register'), {
      'street': ShippingAddressFactory.street,
      'town': '',
      'firstname': '',
      'surname': ShippingAddressFactory.surname,
      'client': client_chosen})

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    request.user = client_chosen.user
    response = add_shipping(request)
    response.client = Client()

    self.assertEqual(ShippingAddress.objects.count(), 0)
    self.assertEqual(response.status_code, 200)


class TestChangeShippingAddress(TestCase):

  def test_change_shipping_get_not_existing(self):
    url = reverse('change_shipping_address')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, change_shipping)

    request = self.factory.get('/change_shipping_address')
    request.COOKIES['device'] = ClientFactory().device
    response = change_shipping(request)
    response.client = Client()

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/add_shipping_address')

  def test_change_shipping_get_existing(self):
    url = reverse('change_shipping_address')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, change_shipping)
    shipping_address = ShippingAddressFactory()

    request = self.factory.get('/change_shipping_address', {'shipping_address': shipping_address})
    request.COOKIES['device'] = shipping_address.client.device

    response = change_shipping(request)
    response.client = Client()

    self.assertEqual(response.status_code, 200)
    self.assertIn(shipping_address.town, str(response.content))
    self.assertIn(shipping_address.street, str(response.content))
    self.assertIn(shipping_address.firstname, str(response.content))
    self.assertIn(shipping_address.surname, str(response.content))

  def test_change_shipping_post_success_not_logged(self):
    url = reverse('change_shipping_address')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, change_shipping)
    shipping_address = ShippingAddressFactory()

    request = self.factory.post('/change_shipping_address', {'shipping_address': shipping_address,
                                                             'town': 'dummy_town',
                                                             'street': 'dummy_street',
                                                             'firstname': shipping_address.firstname,
                                                             'surname': shipping_address.surname})

    request.COOKIES['device'] = shipping_address.client.device

    response = change_shipping(request)
    response.client = Client()
    self.assertEqual(response.status_code, 302)
    self.assertEqual(ShippingAddress.objects.count(), 1)
    self.assertRedirects(response, '/')
    self.assertEqual(ShippingAddress.objects.get().town, 'dummy_town')
    self.assertEqual(ShippingAddress.objects.get().street, 'dummy_street')

  def test_change_shipping_post_success_logged(self):
    url = reverse('change_shipping_address')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, change_shipping)
    shipping_address = ShippingAddressFactoryLogged()

    request = self.factory.post('/change_shipping_address', {'shipping_address': shipping_address,
                                                             'town': 'dummy_town',
                                                             'street': 'dummy_street',
                                                             'firstname': shipping_address.firstname,
                                                             'surname': shipping_address.surname})
    request.user = shipping_address.client.user
    response = change_shipping(request)
    response.client = Client()

    self.assertEqual(response.status_code, 302)
    self.assertEqual(ShippingAddress.objects.count(), 1)
    self.assertRedirects(response, '/')
    self.assertEqual(ShippingAddress.objects.get().town, 'dummy_town')
    self.assertEqual(ShippingAddress.objects.get().street, 'dummy_street')

  def test_change_shipping_post_failed(self):
    url = reverse('change_shipping_address')
    self.factory = RequestFactory()
    self.assertEqual(resolve(url).func, change_shipping)
    shipping_address = ShippingAddressFactory()

    request = self.factory.post('/change_shipping_address',
                                {'town': '',
                                 'street': '',
                                 'firstname': '',
                                 'surname': ''})
    request.COOKIES['device'] = shipping_address.client.device

    response = change_shipping(request)
    response.client = Client()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(ShippingAddress.objects.get().town, shipping_address.town)
    self.assertEqual(ShippingAddress.objects.get().street, shipping_address.street)
    self.assertEqual(ShippingAddress.objects.get().firstname, shipping_address.firstname)
    self.assertEqual(ShippingAddress.objects.get().surname, shipping_address.surname)
