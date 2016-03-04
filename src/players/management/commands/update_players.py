from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

import requests
import kronos
from nba_py.constants import CURRENT_SEASON
from nba_py.player import PlayerList

from players.models import Player, Team


@kronos.register('0 0 * * *')  # Once a day
class Command(BaseCommand):
    help = 'Add/update all NBA players from current season'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip',
            action='store_true',
            dest='skip',
            default=False,
            help='Skip existing players',
        )

    def handle(self, *args, **options):
        all_players = PlayerList().info()

        for api_player in all_players:
            # Get the player, or create him if doesn't exist
            qs = Player.objects.filter(PERSON_ID=api_player['PERSON_ID'])
            if qs.exists():
                player = qs[0]

                if options['skip']:
                    continue
            else:
                player = Player()

            try:
                name = api_player['DISPLAY_LAST_COMMA_FIRST']
                last, first = name.replace(' ', '').split(',', 1)
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

            # Add player photo only on creation
            if not player.photo:
                base_url = ('http://i.cdn.turner.com/nba/nba/.element/'
                            'img/2.0/sect/statscube/players/large/')
                filename = api_player['PLAYERCODE'] + '.png'
                photo_url = base_url + filename

                # Try three times
                session = requests.Session()
                adapter = requests.adapters.HTTPAdapter(max_retries=3)
                session.mount('http://', adapter)
                response = session.get(photo_url)

                if response:
                    image_content = ContentFile(response.content)
                    player.photo.save(filename, image_content)

            player.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated players"))
