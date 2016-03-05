from django import template

register = template.Library()


@register.filter
def percentage(value):
    if value > 0.0:
        return '{0:.1%}'.format(value)
    else:
        return None


@register.assignment_tag
def get_version():
    """Returns app version"""
    from nba_rank import __version__
    return __version__
