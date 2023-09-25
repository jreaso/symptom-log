from django import template

register = template.Library()

@register.filter
def rangefilter(value):
    return range(1, value + 1)