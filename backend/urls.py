"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from clients import views as client_views
from cart import views as cart_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', cart_views.view_cart, name='cart_view'),
    path('login/', auth_views.LoginView.as_view(template_name='clients/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='clients/logout.html'), name='logout'),
    path('register/', client_views.register, name="register"),
    path('profile/', client_views.client_profile, name="profile"),
    path('cart/add/', cart_views.add_to_cart, name="add_to_cart"),
    path('cart/delete/', cart_views.delete_from_cart, name="delete_from_cart"),
    path('cart/delete_all', cart_views.delete_all_from_cart, name="delete_all_from_cart"),
    path('validate_username', client_views.validate_username, name='validate_username'),
    path('add_shipping_address', client_views.add_shipping, name='add_shipping_address'),
    path('change_shipping_address', client_views.change_shipping, name='change_shipping_address'),
    path('checkout', cart_views.checkout, name='checkout')

]
handler500 = 'cart.views.this_server_error'
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)