from django.contrib import admin

from misc.readonly_admin import ReadOnlyModelAdmin
from players.models import Player


@admin.register(Player)
class PlayerAdmin(ReadOnlyModelAdmin):
    list_display = ('PERSON_ID', 'first_name', 'last_name')
