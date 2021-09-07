from django.shortcuts import render, get_object_or_404
from .models import Product, HomepagePromotional, Category
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


class CategoryView(ListView):
    model = Product
    template_name = 'store/products.html'
    context_object_name = 'product'
    MEDIA_URL = '/uploads/'

    def get_queryset(self):
        category = get_object_or_404(Category, name__iexact=self.kwargs.get('name'))
        return Product.objects.filter(category=category)
