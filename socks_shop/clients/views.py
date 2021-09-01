from django.shortcuts import render, redirect
from .forms import ClientRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def register(request):
  if request.method == 'POST':
    form = ClientRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}, please login')
      return redirect('login')
  else:
    form = ClientRegisterForm()
  return render(request, 'clients/register.html', {'form': form})


@login_required
def client_profile(request):
  user = User.objects.get(username=request.user.username)
  context = {
    "user": user,
    'date_joined': user.date_joined
  }
  return render(request, 'clients/profile.html', context)
