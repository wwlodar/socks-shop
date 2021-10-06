from django.contrib import admin
from .models import Client, ShippingAddress


admin.site.register(Client)
admin.site.register(ShippingAddress)