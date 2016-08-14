from django.contrib import admin

from misc.readonly_admin import ReadOnlyModelAdmin
from seasons.models import Season, PlayerSeason


@admin.register(Season)
class SeasonAdmin(ReadOnlyModelAdmin):
    list_display = ('abbr',)


@admin.register(PlayerSeason)
class PlayerSeasonAdmin(ReadOnlyModelAdmin):
    list_display = ('player', 'season', 'team',  'rating_mu', 'rating_sigma',
                    'pts', 'reb', 'ast', 'stl', 'blk',
                    'fg_pct', 'fg3_pct', 'ft_pct')
    list_filter = ('player', 'season', 'team')
