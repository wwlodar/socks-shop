from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Client, ShippingAddress
from django.utils.http import is_safe_url


def validate_username(request):
  username = request.GET.get('username', None)
  response = {
    'is_taken': User.objects.filter(username__iexact=username).exists()
  }
  return JsonResponse(response)


def get_client(request):
  try:
    client = Client.objects.get(user=request.user)
    return client
  except:
    device = request.COOKIES['device']
    client = Client.objects.get(device=device)
    return client


def return_previous_page(request):
  next = request.GET.get('next')
  if not is_safe_url(url=next, allowed_hosts=request.get_host()):
    next = 'home'
  return (next)
