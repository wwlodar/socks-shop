import os
import requests
import logging
import json
from clients.functions import *
from cart.models import Order
import socket

logger = logging.getLogger(__name__)
CURRENCY_CODE = "PLN"


def request_payu_token(
    url='https://secure.snd.payu.com/pl/standard/user/oauth/authorize',
    client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret']
):
  values = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
  }

  response = requests.post(url, values)

  if response.status_code == 200:
    logger.info(f'replied with {response.status_code}')
    try:
      data = json.loads(response.text)
    except ValueError:
      return None
    return data.get('access_token')
  else:
    print(f'Response status_code == {response.status_code}')
    return None


def send_payu_order(
    request,
    url='https://secure.snd.payu.com/api/v2_1/orders', ):
  logger.debug('creating new order')
  client_ip = socket.gethostbyname(socket.gethostname())
  client = get_client(request)
  order = Order.objects.filter(client=client, payment_status='NEW').order_by('-date_of_order')[0]
  if request.user.is_authenticated:
    email = request.user.email
  else:
    email = request.session.get('email')

  products = []
  for product in order.products.all():
    products.append({"name": product.product_in_size.product.name,
                     "unitPrice": product.get_total_item_price(),
                     "quantity": product.quantity})
  payload = json.dumps({
    "notifyUrl": "https://socks-shop.herokuapp.com/notify",
    "continueUrl": "https://socks-shop.herokuapp.com/after_payment",
    "customerIp": client_ip,
    "merchantPosId": os.environ['pos_id'],
    "description": 'Order from socks-shop',
    "currencyCode": CURRENCY_CODE,
    "totalAmount": order.total_price * 100,
    "extOrderId": str(order.pk),
    "buyer": {
      "email": email,
      "firstName": client.shippingaddress.firstname,
      "lastName": client.shippingaddress.surname
    },
    "products": products

  })
  token = str(request_payu_token())
  authorization_bearer = f'Bearer {token}'
  headers = {
    "content-type": "application/json",
    "Authorization": authorization_bearer,
  }

  response = requests.post(
    url=url,
    data=payload,
    headers=headers,
    allow_redirects=False
  )

  if response.status_code == 302:

    try:
      data = json.loads(response.text)
      url = data.get('redirectUri')
      logger.debug(f"redirectUr == {url} and it's status {data.get('status')}")

      if url:
        return url
      else:
        logger.error(
          u"Invalid PayU response, no redirectUri found."
        )
    except ValueError:
      logger.error(
        u"Invalid PayU response."
      )
  if response.status_code == 403:
    print('Not allowed on PayU server - error 403! Check your configuration!')

  if response.status_code == 401:
    print('Error 401, Check your token, authorization seems to be the problem.')
  else:
    print(
      f"Invalid PayU order status code {response.status_code}, check your code."
    )

  return None
