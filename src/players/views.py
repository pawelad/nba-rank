from django.views.generic import ListView

from ranking import Ranking

from players.models import Player


class PlayerListView(ListView):
    template_name = 'players/list.html'
    model = Player

    def get_context_data(self, **kwargs):
        qs = super().get_queryset()

        # Create players ranking
        ranking = Ranking(qs, start=1, key=lambda x: x.rating_mu or 0)
        kwargs['players_ranking'] = ranking

        return super().get_context_data(**kwargs)
