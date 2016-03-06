from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from nba_py.constants import CURRENT_SEASON
from trueskill import Rating, MU, SIGMA


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


class PlayerSeason(TimeStampedModel, models.Model):
    player = models.ForeignKey(
        'players.Player', related_name='seasons',
        verbose_name=_("player"),
    )

    team = models.ForeignKey(
        'players.Team', related_name='players_seasons',
        verbose_name=_("team"),
        null=True,
    )

    season = models.CharField(
        verbose_name=_("season"),
        max_length=16,
    )

    # trueskill
    rating_mu = models.FloatField(
        verbose_name=_("Rating MU"),
        default=MU,
    )

    rating_sigma = models.FloatField(
        verbose_name=_("Rating SIGMA"),
        default=SIGMA,
    )

    # Stats
    pts = models.FloatField(verbose_name="PTS")
    reb = models.FloatField(verbose_name="REB")
    ast = models.FloatField(verbose_name="AST")
    stl = models.FloatField(verbose_name="STL")
    blk = models.FloatField(verbose_name="BLK")
    fg_pct = models.FloatField(verbose_name="FG%")
    fg3_pct = models.FloatField(verbose_name="3P%")
    ft_pct = models.FloatField(verbose_name="FT%")

    # NBA API
    ROSTERSTATUS = models.PositiveSmallIntegerField(
        verbose_name="ROSTERSTATUS",
    )

    GAMES_PLAYED_FLAG = models.CharField(
        verbose_name="GAMES_PLAYED_FLAG",
        max_length=8,
    )

    class Meta:
        verbose_name = _("player season")
        verbose_name_plural = _("player seasons")
        ordering = ['-season', '-rating_mu', 'rating_sigma']
        unique_together = ('player', 'season')

    def get_team_name(self):
        """Return player's season team name."""
        if self.team:
            return '{0.city} {0.name}'.format(self.team)
        else:
            return _("No team")

    def get_rating(self):
        """Return current `Rating` instance with data from database."""
        return Rating(mu=self.rating_mu, sigma=self.rating_sigma)

    def __str__(self):
        return '{0.player} ({0.season})'.format(self)


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
