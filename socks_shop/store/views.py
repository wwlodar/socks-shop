from django.shortcuts import render, get_object_or_404
from .models import Product, HomepagePromotional, Category, Sizes
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.core import serializers
from .forms import AddSizeForm
from django.urls import reverse
from django.http import HttpResponseForbidden


class HomeView(TemplateView):
  template_name = 'store/home.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['promotional_data'] = HomepagePromotional.objects.first()
    return context


class ProductsView(ListView):
  model = Product
  template_name = 'store/products.html'
  context_object_name = 'product'
  MEDIA_URL = '/uploads/'
  ordering_by = ['date_posted']


class ProductDetailView(FormMixin, DetailView):
  form_class = AddSizeForm
  model = Product

  def get_success_url(self):
    return reverse('product-detail', kwargs={'pk': self.object.pk})

  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseForbidden()
    self.object = self.get_object()
    form = self.get_form()
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):
    return super().form_valid(form)

  def get_form_kwargs(self, *args, **kwargs):
    kwargs = super(ProductDetailView, self).get_form_kwargs(*args, **kwargs)
    kwargs['pk'] = self.kwargs['pk']
    return kwargs


class CategoryView(ListView):
  model = Product
  template_name = 'store/products.html'
  context_object_name = 'product'
  MEDIA_URL = '/uploads/'

  def get_queryset(self):
    category = get_object_or_404(Category, name__iexact=self.kwargs.get('name'))
    return Product.objects.filter(category=category)


def get_json_model_data(request, **kwargs):
  pk = kwargs.get('size_pk')
  selected_size = Sizes.objects.filter(pk=pk)
  data = list(selected_size.values())
  return JsonResponse({'data': data})


