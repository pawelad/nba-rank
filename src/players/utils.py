from players.models import Player, Team

from nba_py.constants import CURRENT_SEASON, TEAMS
from nba_py.player import PlayerList


def get_all_players():
    """Get all NBA players from current season and add/update them."""
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


def populate_teams():
    """Add teams to database from nba_py constants."""
    for team in TEAMS.values():
        Team.objects.get_or_create(
            TEAM_ID=team['id'],
            TEAM_CODE=team['code'],
            name=team['name'],
            city=team['city'],
            abbr=team['abbr'],
        )
