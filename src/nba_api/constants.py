"""
Constants needed to interact with the NBA API.
"""
from datetime import datetime

_curr_year = datetime.now().year
if datetime.now().month > 6:
    CURRENT_SEASON = str(_curr_year) + "-" + str(_curr_year + 1)[2:]
else:
    CURRENT_SEASON = str(_curr_year - 1) + "-" + str(_curr_year)[2:]

NBA_LEAGUE_ID = '00'
