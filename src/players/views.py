from django.views.generic import ListView, TemplateView

from ranking import Ranking

from players.models import Player
from misc.utils import get_two_random


class PlayerListView(ListView):
    template_name = 'players/list.html'
    model = Player

    def get_context_data(self, **kwargs):
        qs = super().get_queryset()

        # Create players ranking
        ranking = Ranking(qs, start=1, key=lambda x: x.rating_mu or 0)
        kwargs['players_ranking'] = ranking

        return super().get_context_data(**kwargs)


class PlayerVoteView(TemplateView):
    template_name = 'players/vote.html'

    def get_context_data(self, **kwargs):
        player_a, player_b = get_two_random(Player)
        kwargs['player_a'] = player_a
        kwargs['player_b'] = player_b

        return super().get_context_data(**kwargs)
