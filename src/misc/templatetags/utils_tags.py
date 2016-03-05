from django import template

register = template.Library()


@register.filter
def percentage(value):
    if value > 0.0:
        return '{0:.1%}'.format(value)
    else:
        return None
