"""
NBA API wrapper exceptions.
"""


class NBAException(Exception):
    """
    Base NBA API wrapper exception.
    """
    pass


class InvalidAPIResponse(NBAException):
    """
    Invalid NBA API response exceptions.
    """
    pass
