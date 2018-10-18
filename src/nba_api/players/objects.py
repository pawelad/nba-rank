"""
NBA players related objects.
"""
from nba_api.base import BaseNBAObject
from nba_api.utils import str_to_bool


class Player(BaseNBAObject):
    """
    NBA player representation.
    """
    _required_keys = [
        'display_first_last',
        'display_last_comma_first',
        'from_year',
        'games_played_flag',
        'person_id',
        'playercode',
        'rosterstatus',
        'team_abbreviation',
        'team_city',
        'team_code',
        'team_id',
        'team_name',
        'to_year',
    ]

    _field_mapping = {
        'from_year': int,
        'games_played_flag': str_to_bool,
        'to_year': int,
    }

    def photo(self):
        """
        Returns official player photo URL

        :returns: player photo URL
        :rtype: str
        """
        photo_url = (
            f'http://i.cdn.turner.com/nba/nba/.element/'
            f'img/2.0/sect/statscube/players/large/'
            f'{self.playercode}.png'
        )
        return photo_url

    def __repr__(self):
        return f'<Player: {self.display_first_last} ({self.person_id})>'
