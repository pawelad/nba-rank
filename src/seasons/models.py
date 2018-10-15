from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from trueskill import Rating, MU, SIGMA


class Season(TimeStampedModel, models.Model):
    abbr = models.CharField(
        verbose_name=_("season"),
        max_length=16,
    )

    class Meta:
        verbose_name = _("season")
        verbose_name_plural = _("seasons")
        ordering = ['-abbr']

    def __str__(self):
        return self.abbr


class PlayerSeason(TimeStampedModel, models.Model):
    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE,
        related_name='seasons',
        verbose_name=_("player"),
    )

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_NULL,
        related_name='players_seasons',
        verbose_name=_("team"),
        null=True,
    )

    season = models.ForeignKey(
        'seasons.Season',
        on_delete=models.CASCADE,
        related_name='players_seasons',
        verbose_name=_("season"),
    )

    # Mostly counting overall number of votes while
    # not creating another model just for it
    votes_win = models.PositiveIntegerField(
        verbose_name=_("votes win"),
        default=0,
        editable=False,
    )

    votes_tie = models.PositiveIntegerField(
        verbose_name=_("votes tie"),
        default=0,
        editable=False,
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
