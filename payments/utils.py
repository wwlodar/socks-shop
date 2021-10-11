import os
import requests
import logging
import json
from clients.models import *
from requests import Request, Session
from clients.functions import *
from django.conf import settings
from cart.models import Order
from django.urls import reverse

logger = logging.getLogger(__name__)
CURRENCY_CODE = "PLN"


def request_payu_token(
    url='https://secure.snd.payu.com/pl/standard/user/oauth/authorize',
    client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret']
):
  """
  Returns PayU Token needed to start the transaction
  :param url: URl to payU API
  :param client_id: taken from settings
  :param client_secret: taken from settings
  :return: Token or None if not possible
  """
  logger.info('Requesting PayU TOKEN!')
  values = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
  }

  response = requests.post(url, values)
  logger.info(f'The response is: {response} {response.status_code} {response.content}')

  if response.status_code == 200:
    logger.info(f'replied with {response.status_code}')
    try:
      data = json.loads(response.text)
    except ValueError:
      return None
    return data.get('access_token')
  else:
    logger.debug(f'Response status_code == {response.status_code}')
    return None


import socket


def send_payu_order(
    request,
    url='https://secure.snd.payu.com/api/v2_1/orders', ):
  logger.debug('creating new order')
  client_ip = socket.gethostbyname(socket.gethostname())
  client = get_client(request)
  order = Order.objects.filter(client=client, payment_status='NEW').order_by('-date_of_order')[0]
  payload = json.dumps({
    "notifyUrl": "https://socks-shop.herokuapp.com//notify",
    "continueUrl": "https://socks-shop.herokuapp.com/",
    "customerIp": client_ip,
    "merchantPosId": os.environ['pos_id'],
    "description": 'Order from socks-shop',
    "currencyCode": CURRENCY_CODE,
    "totalAmount": order.total_price * 100,
    "extOrderId": str(order.pk),
    "buyer": {
      "email": 'email@google.com',
      "firstName": client.shippingaddress.firstname,
      "lastName": client.shippingaddress.surname
    },
    "products": [
      {
        "name": 'order.product.name',
        "unitPrice": '10',
        "quantity": "1"
      }

    ],

  })
  token = str(request_payu_token())
  authorization_bearer = f'Bearer {token}'
  print(payload)
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
  print(response.content)

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
