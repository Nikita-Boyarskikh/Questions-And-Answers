from django import template
register = template.Library()  # pylint: disable=invalid-name


@register.filter
def to_class_name(value):
    return value.__class__.__name__
