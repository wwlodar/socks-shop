# socks-shop [![wwlodar](https://circleci.com/gh/wwlodar/socks-shop.svg?style=shield)](https://app.circleci.com/pipelines/github/wwlodar/socks-shop?branch=main)

### Overview
E-commerce website with PayU-integration.
### Demo
Here is a working live demo : https://socks-shop.herokuapp.com/
### Technology
Python 3.9.7. 
Django 3.2.6

### Integrations
PayU Integration requires 'REST API' (Checkout) points of sales (POS).
They can be obtained by registering an account via Sandbox (https://registration-merch-prod.snd.payu.com/boarding/#/registerSandbox/)
or you can also use example Configuration Keys provided by Sandbox. 
![img.png](img.png)

### Installation

First clone the repository from Github and switch to the new directory:
```
$ git clone https://github.com/wwlodar/socks-shop.git
$ cd socks-shop
```
Activate the virtualenv for your project.

Install project dependencies:
```
$ pip install -r requirements.txt
```

You can now run the development server:
```
$ python manage.py runserver
```

