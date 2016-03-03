from django.core.management.base import BaseCommand

import kronos
from nba_py.constants import CURRENT_SEASON
from nba_py.player import PlayerList

from players.models import Player, Team


@kronos.register('0 0 * * *')  # Once a day
class Command(BaseCommand):
    help = 'Add/update all NBA players from current season'

    def handle(self, *args, **options):
        all_players = PlayerList().info()

        for api_player in all_players:
            # Get the player, or create him if doesn't exist
            qs = Player.objects.filter(PERSON_ID=api_player['PERSON_ID'])
            if qs.exists():
                player = qs[0]
            else:
                player = Player()

            try:
                last, first = api_player['DISPLAY_LAST_COMMA_FIRST'].split(',', 1)
            except ValueError:
                # Only one name
                first = api_player['DISPLAY_LAST_COMMA_FIRST']
                last = ''
            player.first_name = first
            player.last_name = last

            if api_player['TEAM_ID'] and api_player['TEAM_CODE']:
                team = Team.objects.get(TEAM_ID=api_player['TEAM_ID'])
            else:
                # Player played this season, but was cut/moved to D-League
                team = None
            player.team = team

            player.season = CURRENT_SEASON
            player.PERSON_ID = api_player['PERSON_ID']
            player.PLAYERCODE = api_player['PLAYERCODE']
            player.ROSTERSTATUS = api_player['ROSTERSTATUS']
            player.GAMES_PLAYED_FLAG = api_player['GAMES_PLAYED_FLAG']
            player.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated players"))
