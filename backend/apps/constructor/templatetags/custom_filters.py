from django import template

register = template.Library()


@register.filter
def split(value, delimiter="\n"):
    if not isinstance(value, str):
        return []
    return value.split(delimiter)
