"""
NBA players related API resources.
"""
from nba_api import constants
from nba_api.base import BaseNBAAPI
from nba_api.players.objects import Player


class PlayersAPI(BaseNBAAPI):
    """
    NBA API players resource.
    """
    def all(self, only_current=True, season=constants.CURRENT_SEASON):
        """
        Lists all NBA players.

        :param only_current: whether to only include current players
        :type only_current: bool
        :param season: NBA season in format YYYY-YY
        :type season: str
        :returns: all NBA players
        :rtype: list of nba.players.Player
        """
        endpoint = 'commonallplayers'
        params = {
            'LeagueID': constants.NBA_LEAGUE_ID,
            'Season': season,
            'IsOnlyCurrentSeason': int(only_current),
        }

        response = self._get_response(endpoint=endpoint, params=params)
        parsed_response = self._parse_response(response.json())

        players = [Player(player_data) for player_data in parsed_response]

        return players
