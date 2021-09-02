from django.db import models
from PIL import Image


class HomepagePromotional(models.Model):
  text = models.CharField(max_length=100)
  image = models.ImageField(upload_to='promotional_pictures')


class Product(models.Model):
  name = models.CharField(max_length=60)
  price = models.IntegerField(default=0)
  quantity = models.IntegerField(null=True)
  description = models.CharField(max_length=250, default='', blank=True, null= True)
  image = models.ImageField(upload_to='products')

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.image.path)
