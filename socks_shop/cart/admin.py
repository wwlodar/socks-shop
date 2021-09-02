from django.contrib import admin
from .models import Cart, OrderedProduct

admin.site.register(Cart)
admin.site.register(OrderedProduct)