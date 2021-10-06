from django.contrib import admin
from .models import Product, HomepagePromotional, Category, Sizes

admin.site.register(Product)
admin.site.register(HomepagePromotional)
admin.site.register(Category)


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
  list_display = ("size_type", "quantity", "product")

