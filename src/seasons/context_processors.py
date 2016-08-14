from seasons.models import Season


def seasons(request):
    """Add available seasons to context."""
    available_seasons = Season.objects.all()

    return {'available_seasons': available_seasons}
