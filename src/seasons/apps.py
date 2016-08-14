from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SeasonsAppConfig(AppConfig):
    name = 'seasons'
    verbose_name = _("seasons")
