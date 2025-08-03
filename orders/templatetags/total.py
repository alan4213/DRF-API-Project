from django import template


register=template.Library()

@register.simple_tag(name='total')

def total(cart):

    tot=0

    for item in cart.order_items.all(): 
        tot+=item.quantity*item.product.price

    return tot