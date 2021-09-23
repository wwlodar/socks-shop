from django import template
from store.models import Category
from cart.models import Cart
from clients.models import Client

register = template.Library()


@register.inclusion_tag('show_categories.html')
def show_categories():
  categories = Category.objects.all()
  return {'categories': categories}


@register.filter
def cart_item_count(request):
  if request.user.is_authenticated:
    client, created = Client.objects.get_or_create(user=request.user)
  else:
   if 'device' in request.COOKIES:
    device = request.COOKIES['device']
    client, created = Client.objects.get_or_create(device=device)
   else:
      return 0

  current_cart = Cart.objects.filter(client=client)
  if current_cart.exists():
    current_cart = current_cart[0]
    number = 0
    for item in current_cart.products.all():
      number += item.quantity
    return number
  else:
    return 0


@register.simple_tag(takes_context=True)
def set_breakpoint(context):
  breakpoint()
