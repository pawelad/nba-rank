from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

import requests
import kronos
from nba_py.player import PlayerList, PlayerGeneralSplits

from players.models import Player, Team, PlayerSeason


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
                if options['skip']:
                    continue

                player = qs[0]
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
            player.PERSON_ID = api_player['PERSON_ID']
            player.PLAYERCODE = api_player['PLAYERCODE']

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

            # Player current season
            player_stats = PlayerGeneralSplits(
                api_player['PERSON_ID']
            ).overall()[0]

            qs = PlayerSeason.objects.filter(
                player=player, season=player_stats['GROUP_VALUE']
            )
            if qs.exists():
                if options['skip']:
                    continue

                player_season = qs[0]
            else:
                player_season = PlayerSeason()

            # Team
            if api_player['TEAM_ID'] and api_player['TEAM_CODE']:
                team = Team.objects.get(TEAM_ID=api_player['TEAM_ID'])
            else:
                # Player played this season, but was cut/moved to D-League
                team = None
            player_season.team = team

            player_season.player = player
            player_season.season = player_stats['GROUP_VALUE']

            player_season.ROSTERSTATUS = api_player['ROSTERSTATUS']
            player_season.GAMES_PLAYED_FLAG = api_player['GAMES_PLAYED_FLAG']

            player_season.pts = player_stats['PTS']
            player_season.reb = player_stats['REB']
            player_season.ast = player_stats['AST']
            player_season.stl = player_stats['STL']
            player_season.blk = player_stats['BLK']
            player_season.fg_pct = player_stats['FG_PCT']
            player_season.fg3_pct = player_stats['FG3_PCT']
            player_season.ft_pct = player_stats['FT_PCT']

            player_season.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated players"))
