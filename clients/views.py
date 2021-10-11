from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ShippingAddressForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Client, ShippingAddress
from django.views.generic.edit import UpdateView
from django.utils.http import is_safe_url
from .functions import *
from cart.models import Order


def register(request):
  device = request.COOKIES['device']
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():

      form.save()
      client = Client.objects.get(device=device)
      username = form.cleaned_data.get('username')
      user = User.objects.get(username=username)
      client.user = user
      client.save()
      messages.success(request, f'Account created for {username}, please login')
      return redirect('login')
    else:
      return render(request, 'clients/register.html', {'form': form})
  else:
    form = UserRegisterForm()
  return render(request, 'clients/register.html', {'form': form})


@login_required
def client_profile(request):
  user = User.objects.get(username=request.user.username)
  client, created = Client.objects.get_or_create(user=request.user)
  orders = Order.objects.filter(client=client)
  shipping_address = ShippingAddress.objects.filter(client=client)
  if shipping_address.exists():
    shipping_address = ShippingAddress.objects.get(client=client)
  else:
    shipping_address = None
  if orders.exists():
    orders = Order.objects.filter(client=client).all
  else:
    orders = None
  context = {
    'user': user,
    'date_joined': user.date_joined,
    'client': client,
    'shipping_address': shipping_address,
    'orders' : orders
  }
  return render(request, 'clients/profile.html', context)


def add_shipping(request):
  if request.method == 'POST':
    form = ShippingAddressForm(request.POST)
    if form.is_valid():
      form_not_saved = form.save(commit=False)
      form_not_saved.client = get_client(request)
      form_not_saved.save()

      return redirect(return_previous_page(request))
  else:
    form = ShippingAddressForm()
  return render(request, 'clients/add_shipping_address.html', {'form': form})


def change_shipping(request):
  shipping_address = ShippingAddress.objects.filter(client=get_client(request))
  if shipping_address.exists():
    shipping_address = ShippingAddress.objects.get(client=get_client(request))
    if request.method == 'POST':
      form = ShippingAddressForm(request.POST, instance=shipping_address)
      if form.is_valid():
        form.save()

        return redirect(return_previous_page(request))
    else:
      form = ShippingAddressForm(instance=shipping_address)
    return render(request, 'clients/change_shipping_address.html', {'form': form})
  else:
    return redirect('add_shipping_address')
