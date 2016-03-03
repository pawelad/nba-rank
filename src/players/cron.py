import kronos

from players import utils


@kronos.register('0 0 * * *')  # Once a day
def get_all_players():
    utils.get_all_players()
