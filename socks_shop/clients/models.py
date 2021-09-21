from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True, blank=True)
  device = models.CharField(max_length=200, null=True, blank=True)
