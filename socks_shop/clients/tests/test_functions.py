from ..functions import *
from .factories import *


class TestGetClient(TestCase):

  def test_get_client_device(self):
    self.factory = RequestFactory()
    request = self.factory.get('')
    request.COOKIES['device'] = ClientFactory().device
    client = get_client(request)
    self.assertEqual(client.device, ClientFactory().device)

  def test_get_client_user(self):
    self.factory = RequestFactory()
    request = self.factory.get('')
    user = ClientLoggedFactory().user
    request.user = user
    client = get_client(request)
    self.assertEqual(client.user, user)


class TestValidateUsername(TestCase):

  def test_username_is_not_taken(self):
    user = UserFactory()
    self.factory = RequestFactory()
    request = self.factory.get('', {'username': user.username})
    request.user = user
    response = validate_username(request)
    self.assertEqual(response.content, b'{"is_taken": true}')

  def test_username_is_taken(self):
    user = UserFactory()
    self.factory = RequestFactory()
    request = self.factory.get('', {'username': 'dummy_username'})
    request.user = user
    response = validate_username(request)
    self.assertEqual(response.content, b'{"is_taken": false}')


class TestReturnPreviousPage(TestCase):

  def test_return_previous_page_success_profile(self):
    self.factory = RequestFactory()
    request = self.factory.get('', {'next': 'profile'})
    response = return_previous_page(request)
    self.assertEqual(response, 'profile')

  def test_return_previous_page_success_cart(self):
    self.factory = RequestFactory()
    request = self.factory.get('', {'next': 'cart'})
    response = return_previous_page(request)
    self.assertEqual(response, 'cart')
