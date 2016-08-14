from django.contrib import admin

from teams.models import Team
from misc.readonly_admin import ReadOnlyModelAdmin


@admin.register(Team)
class TeamAdmin(ReadOnlyModelAdmin):
    list_display = ('TEAM_ID', 'name', 'city', 'abbr')
