from django.test import TestCase, RequestFactory
from ..utils import *
import mock
from cart.tests.factories import OrderFactory, OrderedProductFactory
from clients.tests.factories import *

from mock import patch
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware


class TestRequestPayuToken(TestCase):
  @patch('requests.post')
  def test_request_200(self, mocked_post):
    mocked_post.return_value.status_code = 200
    access_token = "3e5cac39-7e38-4139-8fd6-30adc06a61bd"
    mocked_post.return_value.text = json.dumps({"access_token": access_token,
                                                "token_type": "bearer",
                                                "refresh_token": "6e265a18-d33e-46d7-ae00-853adebbacfd",
                                                "expires_in": 43199,
                                                "grant_type": "clients_credentials"})
    function = request_payu_token()
    self.assertEqual(function, access_token)

  @patch('requests.post')
  def test_request_other(self, mocked_post):
    mocked_post.return_value.status_code = 404
    function = request_payu_token()
    self.assertEqual(function, None)


class TestSendPayuOrder(TestCase):
  @patch('requests.post')
  @mock.patch('payments.utils.request_payu_token', return_value="3e5cac39-7e38-4139-8fd6-30adc06a61bd")
  def test_correct_302(self, mock_token, mocked_post):
    self.factory = RequestFactory()
    client_not_logged = ClientFactory()
    product = OrderedProductFactory(client=client_not_logged)
    order = OrderFactory(client=client_not_logged, products=[product, ])
    shipping_address = ShippingAddressFactory(client=client_not_logged)
    mock_url = "http://secure.payu.com/pl/standard/co/summary?sessionId=rRrraG6udd1WT6XdRUWccgi19ciGpu16&merchantPosId=200003&timeStamp=1446020685341&showLoginDialog=false&apiToken=872f15ed05fa6c1ca52885256ee66276d42e7dc954b62eac4082147",

    mocked_post.return_value.status_code = 302
    mocked_post.return_value.text = json.dumps({
      "status": {
        "statusCode": "SUCCESS",
      },
      "redirectUri": mock_url,
      "orderId": "WZHF5FFDRJ140731GUEST000P01"
    })
    request = self.factory.get('request_payu_token')
    request.COOKIES['device'] = client_not_logged.device

    request.user = AnonymousUser()
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    response = send_payu_order(request)
    self.assertEqual(response,
                     [
                       "http://secure.payu.com/pl/standard/co/summary?sessionId=rRrraG6udd1WT6XdRUWccgi19ciGpu16&merchantPosId=200003&timeStamp=1446020685341&showLoginDialog=false&apiToken=872f15ed05fa6c1ca52885256ee66276d42e7dc954b62eac4082147"])

  @patch('requests.post')
  @mock.patch('payments.utils.request_payu_token', return_value="3e5cac39-7e38-4139-8fd6-30adc06a61bd")
  def test_incorrect(self, mock_token, mocked_post):
    self.factory = RequestFactory()
    client_not_logged = ClientFactory()
    product = OrderedProductFactory(client=client_not_logged)
    order = OrderFactory(client=client_not_logged, products=[product, ])
    shipping_address = ShippingAddressFactory(client=client_not_logged)
    mock_url = "http://secure.payu.com/pl/standard/co/summary?sessionId=rRrraG6udd1WT6XdRUWccgi19ciGpu16&merchantPosId=200003&timeStamp=1446020685341&showLoginDialog=false&apiToken=872f15ed05fa6c1ca52885256ee66276d42e7dc954b62eac4082147",

    mocked_post.return_value.status_code = 403
    mocked_post.return_value.text = json.dumps({
      "status": {
        "statusCode": "SUCCESS",
      },
      "redirectUri": mock_url,
      "orderId": "WZHF5FFDRJ140731GUEST000P01"
    })
    request = self.factory.get('request_payu_token')
    request.COOKIES['device'] = client_not_logged.device

    request.user = AnonymousUser()
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    response = send_payu_order(request)
    self.assertEqual(response, None)
