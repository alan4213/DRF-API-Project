from django import template

register=template.Library()


@register.simple_tag(name='ostatus')

def ostatus(status):
    status=status-1

    status_array=['confirmed', 'processed', 'delivered', 'rejected']

    return status_array[status]

