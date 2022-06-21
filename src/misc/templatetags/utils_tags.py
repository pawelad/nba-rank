from django import template

register = template.Library()


@register.filter
def percentage(value):
    if value > 0.0:
        return '{0:.1f}'.format(value * 100)
    else:
        return None


@register.simple_tag
def get_version():
    """Return app version."""
    from nba_rank import __version__
    return __version__


@register.simple_tag
def total_votes():
    """Return the total number of votes."""
    from django.db.models import Sum
    from players.models import PlayerSeason
    votes = PlayerSeason.objects.aggregate(win_votes=Sum('votes_win'),
                                           tie_votes=Sum('votes_tie'))
    return int(votes['win_votes'] + (votes['tie_votes'] / 2))
