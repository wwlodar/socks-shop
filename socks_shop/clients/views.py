from django.shortcuts import render, redirect
from .forms import ClientRegisterForm, ShippingAddressForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Client, ShippingAddress
from django.views.generic.edit import UpdateView
from django.utils.http import is_safe_url


def register(request):
  device = request.COOKIES['device']
  if request.method == 'POST':
    form = ClientRegisterForm(request.POST)
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
    form = ClientRegisterForm()
  return render(request, 'clients/register.html', {'form': form})


@login_required
def client_profile(request):
  user = User.objects.get(username=request.user.username)
  client = Client.objects.get(user=request.user)
  shipping_address = ShippingAddress.objects.filter(client=client)
  if shipping_address.exists():
    shipping_address = ShippingAddress.objects.get(client=client)
  else:
    pass
  context = {
    'user': user,
    'date_joined': user.date_joined,
    'client': client,
    'shipping_address': shipping_address
  }
  return render(request, 'clients/profile.html', context)


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
      'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)



def add_shipping(request):
  if request.method == 'POST':
    form = ShippingAddressForm(request.POST)
    if form.is_valid():
      form_not_saved = form.save(commit=False)
      if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
      else:
        device = request.COOKIES['device']
        client = Client.objects.get(device=device)
      form_not_saved.client = client
      form_not_saved.save()

      next = request.GET.get('next')
      if not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = 'home'
      return redirect(next)
  else:
    form = ShippingAddressForm()
  return render(request, 'clients/add_shipping_address.html', {'form': form})


def change_shipping(request):
  if request.user.is_authenticated:
    client = Client.objects.get(user=request.user)
  else:
    device = request.COOKIES['device']
    client = Client.objects.get(device=device)
  shipping_address = ShippingAddress.objects.get(client=client)
  if request.method == 'POST':
    form = ShippingAddressForm(request.POST, instance=shipping_address)
    if form.is_valid():
      form.save()

      next = request.GET.get('next')
      if not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = 'home'
      return redirect(next)
  else:
    form = ShippingAddressForm(instance=shipping_address)
  return render(request, 'clients/change_shipping_address.html', {'form': form})
