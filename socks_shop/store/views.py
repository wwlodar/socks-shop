from django.shortcuts import render
from .models import Product, HomepagePromotional
from django.views.generic import ListView, DetailView


def home(request):
    context = {
        'promotional_data': HomepagePromotional.objects.first()
    }
    return render(request, 'store/home.html', context)


class ProductsView(ListView):
    model = Product
    template_name = 'store/products.html'
    context_object_name = 'product'
    MEDIA_URL = '/uploads/'
    ordering_by = ['date_posted']


class ProductDetailView(DetailView):
  model = Product
  context_object_name = 'product'
