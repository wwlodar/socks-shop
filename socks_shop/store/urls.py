from django.urls import path
from . import views
from .views import ProductsView, ProductDetailView, CategoryView

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', ProductsView.as_view(), name='products_page'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:name>/', CategoryView.as_view(), name='category_view')
]
