from django.core.management.base import BaseCommand

from nba_py.constants import TEAMS

from players.models import Team


class Command(BaseCommand):
    help = 'Add teams to database from nba_py constants'

    def handle(self, *args, **options):
        for team in TEAMS.values():
            Team.objects.get_or_create(
                TEAM_ID=team['id'],
                TEAM_CODE=team['code'],
                name=team['name'],
                city=team['city'],
                abbr=team['abbr'],
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated teams"))
