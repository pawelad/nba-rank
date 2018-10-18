"""
NBA API wrapper utils.
"""


def str_to_bool(value):
    """
    Interpret a string as a bool value.

    :param value: a string to interpret
    :type value: str
    :returns: interpreted value
    :rtype: bool
    """
    return value.lower() in ("yes", "y", "true", "t", "1")
