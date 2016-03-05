from players.models import PlayerSeason


def seasons(request):
    """Add available seasons to context."""
    available_seasons = PlayerSeason.objects.order_by().values_list(
        'season', flat=True
    ).distinct()

    return {'available_seasons': sorted(available_seasons)}
