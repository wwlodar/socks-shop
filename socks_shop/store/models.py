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


class Product(models.Model):
  name = models.CharField(max_length=60)
  price = models.IntegerField(default=0)
  description = models.CharField(max_length=250, default='', blank=True, null= True)
  image = models.ImageField(upload_to='products')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.image.path)


class Sizes(models.Model):
  sm = "small"
  md = "medium"
  lg = "large"
  sizes = [
    (sm, "EU 35-37"),
    (md, "EU 38-40"),
    (lg, "EU 41-43"),
  ]
  size_type = models.CharField(max_length=128, choices=sizes)
  price = models.IntegerField(blank=False)
  date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
  quantity = models.IntegerField(null=True)
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return Product.name, self.size_type
