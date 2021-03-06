from django.db import models
from PIL import Image


class HomepagePromotional(models.Model):
  text = models.CharField(max_length=100)
  image = models.ImageField(upload_to='promotional_pictures')


class Category(models.Model):
  name = models.CharField(max_length=60)
  date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = "Categories"


class Product(models.Model):
  name = models.CharField(max_length=60)
  description = models.CharField(max_length=250, default='', blank=True, null=True)
  image = models.ImageField(upload_to='products')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  
  def __str__(self):
    return f" {str(self.name)}"


class Sizes(models.Model):
  sm = "EU 35-37"
  md = "EU 38-40"
  lg = "EU 41-43"
  sizes = [
    (sm, "EU 35-37"),
    (md, "EU 38-40"),
    (lg, "EU 41-43"),
  ]
  size_type = models.CharField(max_length=128, choices=sizes)
  price = models.IntegerField(blank=False)
  date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
  quantity = models.IntegerField(null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  
  def __str__(self):
    return f" {str(self.size_type)}"
  
  class Meta:
    unique_together = ('size_type', 'product')
    verbose_name_plural = "Sizes"
