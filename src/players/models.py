from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from nba_py.constants import CURRENT_SEASON

from seasons.models import PlayerSeason


class Player(TimeStampedModel, models.Model):
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=64,
    )

    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=64,
    )

    photo = models.ImageField(
        verbose_name=_("photo"),
        upload_to='players_photos',
        null=True,
    )

    # NBA API
    PERSON_ID = models.PositiveIntegerField(
        verbose_name="PERSON_ID",
        unique=True,
    )

    PLAYERCODE = models.CharField(
        verbose_name="PLAYERCODE",
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")
        ordering = ['last_name', 'first_name']

    @cached_property
    def get_full_name(self):
        """Return player name."""
        return ' '.join([self.first_name, self.last_name])

    def get_current_season(self):
        """Return player's current season"""
        return PlayerSeason.objects.get(player=self, season=CURRENT_SEASON)

    def __str__(self):
        return '{0.get_full_name} ({0.PERSON_ID})'.format(self)
