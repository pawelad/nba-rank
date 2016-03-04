from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PlayersAppConfig(AppConfig):
    name = 'players'
    verbose_name = _("players")
