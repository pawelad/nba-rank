from django.views.generic import ListView

from players.models import Player


class PlayerListView(ListView):
    template_name = 'players/list.html'
    model = Player
