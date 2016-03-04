from django.contrib import admin

from misc.readonly_admin import ReadOnlyModelAdmin
from players.models import Player, Team


@admin.register(Player)
class PlayerAdmin(ReadOnlyModelAdmin):
    list_display = ('PERSON_ID', 'first_name', 'last_name', 'team',
                    'rating_mu', 'rating_sigma')
    list_filter = ('team',)


@admin.register(Team)
class TeamAdmin(ReadOnlyModelAdmin):
    list_display = ('TEAM_ID', 'name', 'city', 'abbr')
