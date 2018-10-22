"""
NBA players related objects.
"""
from nba_api.base import BaseNBAObject
from nba_api.utils import str_to_bool


class Player(BaseNBAObject):
    """
    NBA player representation.
    """
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


class PlayerStats(BaseNBAObject):
    """
    NBA player stats representation.
    """

    def __repr__(self):
        return f'<PlayerStats: {self.group_set})>'
