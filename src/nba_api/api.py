"""
Main interface for interacting with the NBA API wrapper.
"""
import requests

from nba_api.players import PlayersAPI


class NBA:
    """
    Main NBA API object that exposes all available resources.
    """

    def __init__(self, session=None):
        """
        Allows passing a custom (requests compatible) session object.

        :param session: custom (requests compatible) session object
        :type session: `requests.Session`
        """
        self._session = session or requests.Session()

        self.players = PlayersAPI(self._session)
