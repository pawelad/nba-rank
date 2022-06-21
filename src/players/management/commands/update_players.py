from random import randint
from time import sleep

import kronos
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from nba_api import NBA
from players.models import Player
from seasons.models import Season, PlayerSeason
from teams.models import Team


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
        nba_api = NBA()
        all_players = nba_api.players.all()

        for api_player in all_players:
            # Get the player, or create him if doesn't exist
            qs = Player.objects.filter(PERSON_ID=api_player.person_id)
            if qs.exists():
                if options['skip']:
                    self.stdout.write(self.style.SUCCESS(f"Skipping {api_player}"))
                    continue

                player = qs.get()
                self.stdout.write(self.style.SUCCESS(f"Updating {api_player}"))
            else:
                player = Player()
                self.stdout.write(self.style.SUCCESS(f"Adding {api_player}"))

            try:
                name = api_player.display_last_comma_first
                last, first = name.replace(' ', '').split(',', 1)
            except ValueError:
                # Only one name
                first = api_player.display_last_comma_first
                last = ''

            player.first_name = first
            player.last_name = last
            player.PERSON_ID = api_player.person_id
            player.PLAYERCODE = api_player.playercode

            # Add player photo only on creation
            # if not player.photo:
            #     # Try three times
            #     response = nba_api._session.get(api_player.photo())
            #
            #     if response:
            #         image_content = ContentFile(response.content)
            #         filename = '_'.join([last, first]).lower()
            #         player.photo.save(f"{filename}.png", image_content)

            player.save()

            # Player current season stats
            player_stats = nba_api.players.stats(api_player.person_id)
            if not player_stats:
                self.stdout.write(self.style.ERROR(f"No stats for {api_player}"))
                continue

            season, _ = Season.objects.get_or_create(
                abbr=player_stats.group_value,
            )

            qs = PlayerSeason.objects.filter(
                player=player, season=season,
            )
            if qs.exists():
                player_season = qs.get()
            else:
                player_season = PlayerSeason()

            # Team
            if api_player.team_id and api_player.team_code:
                team = Team.objects.get(TEAM_ID=api_player.team_id)
            else:
                # Player played this season, but was cut/moved to D-League
                team = None

            player_season.team = team
            player_season.player = player
            player_season.season = season

            player_season.ROSTERSTATUS = api_player.rosterstatus
            player_season.GAMES_PLAYED_FLAG = api_player.games_played_flag

            player_season.pts = player_stats.pts
            player_season.reb = player_stats.reb
            player_season.ast = player_stats.ast
            player_season.stl = player_stats.stl
            player_season.blk = player_stats.blk
            player_season.fg_pct = player_stats.fg_pct
            player_season.fg3_pct = player_stats.fg3_pct
            player_season.ft_pct = player_stats.ft_pct

            player_season.save()

            # Don't spam the API
            sleep(6)

        self.stdout.write(self.style.SUCCESS("Successfully updated players"))
