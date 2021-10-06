def add_quantity(order_item, quantity):
  order_item.quantity += int(quantity)
  order_item.save()