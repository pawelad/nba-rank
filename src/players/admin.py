from django.contrib import admin

from misc.readonly_admin import ReadOnlyModelAdmin
from players.models import Player, PlayerSeason, Team


@admin.register(Player)
class PlayerAdmin(ReadOnlyModelAdmin):
    list_display = ('PERSON_ID', 'first_name', 'last_name')


@admin.register(PlayerSeason)
class PlayerSeasonAdmin(ReadOnlyModelAdmin):
    list_display = ('player', 'season', 'team',  'rating_mu', 'rating_sigma',
                    'pts', 'reb', 'ast', 'stl', 'blk',
                    'fg_pct', 'fg3_pct', 'ft_pct')
    list_filter = ('player', 'season', 'team')


@admin.register(Team)
class TeamAdmin(ReadOnlyModelAdmin):
    list_display = ('TEAM_ID', 'name', 'city', 'abbr')
