from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="username")
def username(value):
    return mark_safe(str(value).split("@")[0])
