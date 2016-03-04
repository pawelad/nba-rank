from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from trueskill import Rating


class Player(TimeStampedModel, models.Model):
    team = models.ForeignKey(
        'players.Team', related_name='players',
        verbose_name=_("team"),
        null=True,
    )

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

    season = models.CharField(
        verbose_name=_("season"),
        max_length=16,
    )

    rating_mu = models.FloatField(
        verbose_name=_("Rating MU"),
        null=True,
        default=None,
    )

    rating_sigma = models.FloatField(
        verbose_name=_("Rating SIGMA"),
        null=True,
        default=None,
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

    ROSTERSTATUS = models.PositiveSmallIntegerField(
        verbose_name="ROSTERSTATUS",
    )

    GAMES_PLAYED_FLAG = models.CharField(
        verbose_name="GAMES_PLAYED_FLAG",
        max_length=8,
    )

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")
        ordering = ['-rating_mu', 'rating_sigma', 'last_name']

    @cached_property
    def get_full_name(self):
        """Return player name."""
        if self.last_name:
            return '{0.first_name} {0.last_name}'.format(self)
        else:
            return self.first_name

    @cached_property
    def get_team_name(self):
        """Return player team name."""
        if self.team:
            return '{0.city} {0.name}'.format(self.team)
        else:
            return _("No team")

    def get_rating(self):
        """Return `Rating` instance with data from database"""
        return Rating(mu=self.rating_mu, sigma=self.rating_sigma)

    def __str__(self):
        return '{0.first_name} {0.last_name} ({0.PERSON_ID})'.format(self)


class Team(TimeStampedModel, models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=128,
    )

    city = models.CharField(
        verbose_name=_("city"),
        max_length=128,
    )

    abbr = models.CharField(
        verbose_name=_("abbreviation"),
        max_length=8,
    )

    # NBA API
    TEAM_ID = models.PositiveIntegerField(
        verbose_name="TEAM_ID",
        unique=True,
    )

    TEAM_CODE = models.CharField(
        verbose_name="TEAM_CODE",
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")
        ordering = ['name']

    def __str__(self):
        return '{0.city} {0.name} ({0.abbr})'.format(self)
