from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel


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
