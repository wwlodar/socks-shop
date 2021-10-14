from django.test import TestCase, RequestFactory, override_settings
from cart.tests.factories import OrderFactory, CartFactory, OrderedProductFactory
from clients.tests.factories import *
from ..views import *

TEST_DIR = 'test_data'


class TestNotifyPayment(TestCase):

  def test_post_new_and_pending_order(self):
    self.factory = RequestFactory()
    order = OrderFactory(pk=100)

    request = self.factory.post('/notify_payment',
                                data=json.dumps({
                                  "order": {
                                    "orderId": "LDLW5N7MF4140324GUEST000P01",
                                    "extOrderId": 100,
                                    "orderCreateDate": "2012-12-31T12:00:00",
                                    "notifyUrl": "http://tempuri.org/notify",
                                    "customerIp": "127.0.0.1",
                                    "merchantPosId": "{Id punktu płatności (pos_id)}",
                                    "description": "Twój opis zamówienia",
                                    "currencyCode": "PLN",
                                    "totalAmount": "200",
                                    "status": "PENDING"
                                  },
                                  "localReceiptDateTime": "2016-03-02T12:58:14.828+01:00",
                                  "properties": [
                                    {
                                      "name": "PAYMENT_ID",
                                      "value": "151471228"
                                    }
                                  ]
                                }),
                                content_type='application/json')

    request.COOKIES['device'] = ClientFactory().device
    response = notify_payment_view(request)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Order.objects.get(pk=100).payment_status, 'NEW')
    self.assertEqual(Order.objects.get(pk=100).status_date, None)

  def test_completed_order(self):
    self.factory = RequestFactory()
    order = OrderFactory(pk=100)

    request = self.factory.post('/notify_payment',
                                data=json.dumps({
                                  "order": {
                                    "orderId": "LDLW5N7MF4140324GUEST000P01",
                                    "extOrderId": 100,
                                    "orderCreateDate": "2012-12-31T12:00:00",
                                    "notifyUrl": "http://tempuri.org/notify",
                                    "customerIp": "127.0.0.1",
                                    "merchantPosId": "{Id punktu płatności (pos_id)}",
                                    "description": "Twój opis zamówienia",
                                    "currencyCode": "PLN",
                                    "totalAmount": "200",
                                    "status": "COMPLETED"
                                  },
                                  "localReceiptDateTime": "2016-03-02T12:58:14.828+01:00",
                                  "properties": [
                                    {
                                      "name": "PAYMENT_ID",
                                      "value": "151471228"
                                    }
                                  ]
                                }),
                                content_type='application/json')

    request.COOKIES['device'] = ClientFactory().device
    response = notify_payment_view(request)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Order.objects.get(pk=100).payment_status, 'COMPLETED')
    self.assertNotEqual(Order.objects.get(pk=100).status_date, None)


class TestAfterPayment(TestCase):
  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_logged(self):
    self.factory = RequestFactory()
    client = ClientLoggedFactory()
    cart = CartFactory(client=client)
    order = OrderFactory(client=client, pk=1)

    request = self.factory.get('/after_payment')
    request.user = client.user

    response = after_payment(request)
    print(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertIn(str(order.pk), str(response.content))
    self.assertIn("Please check details in your profile!", str(response.content))
    self.assertEqual(Cart.objects.filter(client=client).count(), 0)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_not_logged(self):
    self.factory = RequestFactory()
    client = ClientFactory()
    cart = CartFactory(client=client)
    order = OrderFactory(client=client, pk=1)

    request = self.factory.get('/after_payment')
    request.COOKIES['device'] = client.device

    response = after_payment(request)
    print(response.content)
    self.assertEqual(response.status_code, 200)
    self.assertIn(str(order.pk), str(response.content))
    self.assertIn("Thank you for shopping", str(response.content))
    self.assertEqual(Cart.objects.filter(client=client).count(), 0)
