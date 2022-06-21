"""
Base objects implementations.
"""
from urllib.parse import urljoin

import requests
from fake_useragent import UserAgent

from nba_api import exceptions


class BaseNBAAPI:
    """
    Base class for NBA API resources.
    """
    api_url = 'http://stats.nba.com/stats/'
    referer = 'player'

    def __init__(self, session=None):
        """
        Allows passing a custom (requests compatible) session object.

        :param session: custom (requests compatible) session object
        :type session: `requests.Session`
        """
        self._session = session or requests.Session()

    @staticmethod
    def _get_headers():
        """
        Returns headers used when requesting the data from NBA API.
        It's based off and tries to imitate real life requests, as NBA
        is known to block certain types of requests.
        May need to be tweaked in the future.

        :returns: request headers
        :rtype: dict
        """
        user_agent = UserAgent().random

        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en",
            "Host": "stats.nba.com",
            "Origin": "http://stats.nba.com",
            "User-Agent": user_agent,
            "x-nba-stats-origin": "stats",
            "x-nba-stats-token": "true",
        }

        return headers

    @staticmethod
    def _parse_response(response):
        """
        Helper method for parsing the NBA API response.
        It's needed because of response format which separates object values
        and headers.

        :param response: JSON API response
        :type response: dict
        :returns: parsed API response
        :rtype: list of dicts or dict
        """
        if 'resultSets' not in response:
            raise exceptions.InvalidAPIResponse(
                f"Invalid response format: {response}"
            )

        row_headers = response['resultSets'][0]['headers']
        # Row headers are returned in caps
        row_headers = [header.lower() for header in row_headers]
        values = response['resultSets'][0]['rowSet']

        if not values:
            return None

        # Create a list of dictionaries from row headers and the list of values
        objects = [dict(zip(row_headers, value)) for value in values]

        if len(objects) == 1:
            return objects[0]

        return objects

    def _get_response(self, endpoint, method='get', params=None, referer=None):
        """
        Helper method to handle HTTP requests and catch API errors.

        :param endpoint: API endpoint
        :type endpoint: str
        :param method: valid HTTP method
        :type method: str
        :param params: extra parameters passed with the request
        :type params: dict
        :returns: API response
        :rtype: Response
        """
        url = urljoin(self.api_url, endpoint)
        headers = self._get_headers()
        headers['Referer'] = urljoin("http://stats.nba.com/", referer)

        response = getattr(self._session, method)(url, headers=headers, params=params)

        if not response.ok:
            raise exceptions.InvalidAPIResponse(
                f"Something went wrong: {response.json()}"
            )

        return response


class BaseNBAObject:
    """
    Base class for NBA API objects.
    """
    _field_mapping = {}

    def __init__(self, data):
        """
        Takes a (pre-parsed) API response and maps the values as class attributes.
        Casting fields to Python objects (i.e. boolean, dates) is supported with
        '_field_mapping' attribute.

        :param data: API response
        :type data: dict
        """
        self._raw_data = data.copy()

        # Cast custom fields mapping
        for field_name, cast_func in self._field_mapping.items():
            data[field_name] = cast_func(data[field_name])

        self.__dict__.update(**data)
