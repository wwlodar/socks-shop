from django.urls import path
from . import views
from .views import ProductsView, ProductDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', ProductsView.as_view(), name='products_page'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
