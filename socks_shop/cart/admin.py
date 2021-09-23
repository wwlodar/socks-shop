from django.contrib import admin
from .models import Cart, OrderedProduct, Order

admin.site.register(Cart)
admin.site.register(OrderedProduct)
admin.site.register(Order)