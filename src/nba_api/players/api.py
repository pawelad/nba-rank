"""
NBA players related API resources.
"""
from nba_api import constants
from nba_api.base import BaseNBAAPI
from nba_api.players.objects import Player, PlayerStats


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

        response = self._get_response(endpoint=endpoint, params=params, referer='scores')
        parsed_response = self._parse_response(response.json())

        players = [Player(player_data) for player_data in parsed_response]

        return players

    def stats(
        self,
        player_id,
        *,
        date_from=constants.Date.DEFAULT.value,
        date_to=constants.Date.DEFAULT.value,
        game_segment=constants.GameSegment.DEFAULT.value,
        last_n_games=constants.LastNGames.DEFAULT.value,
        location=constants.Location.DEFAULT.value,
        measure_type=constants.MeasureType.DEFAULT.value,
        month=constants.Month.DEFAULT.value,
        opponent_team_id=constants.TeamID.DEFAULT.value,
        outcome=constants.Outcome.DEFAULT.value,
        pace_adjust=constants.PaceAdjust.DEFAULT.value,
        per_mode=constants.PerMode.DEFAULT.value,
        period=constants.Period.DEFAULT.value,
        plus_minus=constants.PlusMinus.DEFAULT.value,
        po_round=constants.PlayoffRound.DEFAULT.value,
        rank=constants.Rank.DEFAULT.value,
        season=constants.CURRENT_SEASON,
        season_segment=constants.SeasonSegment.DEFAULT.value,
        season_type=constants.SeasonType.DEFAULT.value,
        shot_clock_range=constants.ShotClockRange.DEFAULT.value,
        team_id=constants.TeamID.DEFAULT.value,
        vs_conference=constants.VsConference.DEFAULT.value,
        vs_division=constants.VsDivision.DEFAULT.value,
    ):
        endpoint = "playerdashboardbygeneralsplits"
        params = {
            "DateFrom": date_from,
            "DateTo": date_to,
            "GameSegment": game_segment,
            "LastNGames": last_n_games,
            "LeagueID": constants.NBA_LEAGUE_ID,
            "Location": location,
            "MeasureType": measure_type,
            "Month": month,
            "OpponentTeamID": opponent_team_id,
            "Outcome": outcome,
            "PaceAdjust": pace_adjust,
            "Period": period,
            "PerMode": per_mode,
            "PlayerID": player_id,
            "PlusMinus": plus_minus,
            "PORound": po_round,
            "Rank": rank,
            "Season": season,
            "SeasonSegment": season_segment,
            "SeasonType": season_type,
            "ShotClockRange": shot_clock_range,
            "TeamID": team_id,
            "VsConference": vs_conference,
            "VsDivision": vs_division,
        }

        response = self._get_response(endpoint=endpoint, params=params, referer='player')
        parsed_response = self._parse_response(response.json())

        if not parsed_response:
            return None

        player_stats = PlayerStats(parsed_response)

        return player_stats
