from django import template

register = template.Library()

@register.filter
def urlstartswith(value, arg):
    return value.startswith(arg)
