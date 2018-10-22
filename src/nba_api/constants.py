"""
Constants needed to interact with the NBA API.
Adapted from:
    https://github.com/seemethere/nba_py/blob/ffeaf4251d796ff9313367a752a45a0d7b16489e/nba_py/constants.py
"""
from datetime import datetime
from enum import Enum


NBA_LEAGUE_ID = "00"

# Get current season in YYYY-YY format
_curr_year = datetime.now().year
if datetime.now().month > 6:
    CURRENT_SEASON = str(_curr_year) + "-" + str(_curr_year + 1)[2:]
else:
    CURRENT_SEASON = str(_curr_year - 1) + "-" + str(_curr_year)[2:]


class Date(Enum):
    DEFAULT = ""


class GameSegment(Enum):
    ENTIRE_GAME = ""
    FIRST_HALF = "First Half"
    SECOND_HALF = "Second Half"
    OVERTIME = "Overtime"
    DEFAULT = ENTIRE_GAME


class LastNGames(Enum):
    DEFAULT = 0


class Location(Enum):
    ALL = ""
    AWAY = "Away"
    HOME = "Home"
    DEFAULT = ALL


class MeasureType(Enum):
    ADVANCED = "Advanced"
    BASE = "Base"
    FOUR_FACTORS = "Four Factors"
    MISC = "Misc"
    OPPONENT = "Opponent"
    SCORING = "Scoring"
    USAGE = "Usage"
    DEFAULT = BASE


class Month(Enum):
    ALL = "0"
    OCTOBER = "1"
    NOVEMBER = "2"
    DECEMBER = "3"
    JANUARY = "4"
    FEBRUARY = "5"
    MARCH = "6"
    APRIL = "7"
    MAY = "8"
    JUNE = "9"
    JULY = "10"
    AUGUST = "11"
    SEPTEMBER = "12"
    DEFAULT = ALL


class Outcome(Enum):
    ALL = ""
    LOSS = "L"
    WIN = "W"
    DEFAULT = ALL


class PaceAdjust(Enum):
    DEFAULT = "N"


class Period(Enum):
    ALL = "0"
    FIRST_QUARTER = "1"
    SECOND_QUARTER = "2"
    THIRD_QUARTER = "3"
    FOURTH_QUARTER = "4"
    OVERTIME = "5"
    DEFAULT = ALL


class PerMode(Enum):
    MINUTES_PER = "MinutesPer"
    PER_100_PLAYS = "Per100Plays"
    PER_100_POSSESSION = "Per100Possessions"
    PER_36 = "Per36"
    PER_40 = "Per40"
    PER_48 = "Per48"
    PER_GAME = "PerGame"
    PER_MINUTE = "PerMinute"
    PER_PLAY = "PerPlay"
    PER_POSSESSION = "PerPossession"
    TOTALS = "Totals"
    DEFAULT = PER_GAME


class PlayoffRound(Enum):
    ALL = "0"
    QUARTERFINALS = "1"
    SEMIFINALS = "2"
    CONFERENCE_FINALS = "3"
    FINALS = "4"
    DEFAULT = ALL


class PlusMinus(Enum):
    DEFAULT = "N"


class Rank(Enum):
    DEFAULT = "N"


class SeasonSegment(Enum):
    ENTIRE_SEASON = ""
    PRE_ALL_STAR = "Pre All-Star"
    POST_ALL_STAR = "Post All-Star"
    DEFAULT = ENTIRE_SEASON


class SeasonType(Enum):
    PLAYOFFS = "Playoffs"
    REGULAR = "Regular Season"
    DEFAULT = REGULAR


class ShotClockRange(Enum):
    ALL = ""
    VERY_LATE = "4-0 Very Late"
    LATE = "7-4 Late"
    AVERAGE = "15-7 Average"
    EARLY = "18-15 Early"
    VERY_EARLY = "22-18 Very Early"
    VERY_VERY_EARLY = "24-22"
    SHOT_CLOCK_OFF = "ShotClock Off"
    DEFAULT = ALL


class TeamID(Enum):
    DEFAULT = 0


class VsConference(Enum):
    ALL = ""
    EAST = "East"
    WEST = "West"
    DEFAULT = ALL


class VsDivision(Enum):
    ALL = ""
    ATLANTIC = "Atlantic"
    CENTRAL = "Central"
    NORTHWEST = "Northwest"
    PACIFIC = "Pacific"
    SOUTHEAST = "Southeast"
    SOUTHWEST = "Southwest"
    DEFAULT = ALL
