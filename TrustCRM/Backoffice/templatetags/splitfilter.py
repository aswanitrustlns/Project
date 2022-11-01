from django import template

register = template.Library()
@register.filter()
def imagecut(value):
    return value.split(':')