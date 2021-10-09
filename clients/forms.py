from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import ShippingAddress


class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']


class ShippingAddressForm(ModelForm):
  class Meta:
    model = ShippingAddress
    exclude = ['client']



