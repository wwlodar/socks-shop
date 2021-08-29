from django.db import models


class Product(models.Model):
  name = models.CharField(max_length=60)
  price = models.IntegerField(default=0)
  description = models.CharField(max_length=250, default='', blank=True, null= True)
  image = models.ImageField(upload_to='uploads/products/')
