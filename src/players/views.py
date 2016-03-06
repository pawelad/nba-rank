from django.core import signing
from django.views.generic import ListView, TemplateView, View
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _

from trueskill import rate_1vs1
from ranking import Ranking

from players.models import PlayerSeason
from misc.utils import get_two_random


class PlayerListView(ListView):
    template_name = 'players/ranking.html'
    context_object_name = 'players_ranking'
    model = PlayerSeason
    paginate_by = 50

    def get_queryset(self):
        season = self.kwargs['season']
        qs = super().get_queryset().filter(season=season)
        if not qs.exists():
            raise Http404

        # Create players ranking
        ranking = Ranking(qs, start=1, key=lambda x: x.rating_mu or 0)

        return list(ranking)  # Not really a queryset, but helps with pagination

    def get_context_data(self, **kwargs):
        kwargs['season'] = self.kwargs['season']
        return super().get_context_data(**kwargs)


class PlayerVoteModalView(TemplateView):
    template_name = 'players/vote.html'

    def get_context_data(self, **kwargs):
        # Get two random players from given season
        season = self.kwargs['season']
        qs = PlayerSeason.objects.filter(season=season)
        player_season_a, player_season_b = get_two_random(qs)
        kwargs['player_season_a'] = player_season_a
        kwargs['player_season_b'] = player_season_b

        # Create signed keys (only work for 30 seconds)
        # First player passed is the winner; has more then 2 elements if tied
        kwargs['player_season_a_key'] = signing.dumps(
            (player_season_a.pk, player_season_b.pk)
        )
        kwargs['player_season_b_key'] = signing.dumps(
            (player_season_b.pk, player_season_a.pk)
        )
        kwargs['tie_key'] = signing.dumps(
            (player_season_a.pk, player_season_b.pk, True)
        )

        return super().get_context_data(**kwargs)


class PlayerVoteSaveView(View):
    def get(self, request, *args, **kwargs):
        try:
            data = signing.loads(self.kwargs['signed_data'], max_age=30)
        except signing.SignatureExpired:
            messages.info(request, _("Sorry, but your vote link expired. "
                                     "Feel free to vote again."))
            return redirect('index')
        except signing.BadSignature:
            raise Http404

        player_a = get_object_or_404(PlayerSeason, pk=data[0])
        rating_a = player_a.get_rating()
        player_b = get_object_or_404(PlayerSeason, pk=data[1])
        rating_b = player_b.get_rating()

        if player_a.season != player_b.season:
            raise Http404

        if len(data) == 2:
            # First one is the winner
            rating_a, rating_b = rate_1vs1(rating_a, rating_b)
            rating_a.votes += 2
        else:
            # Tie
            rating_a, rating_b = rate_1vs1(rating_a, rating_b, drawn=True)
            rating_a.votes += 1
            rating_b.votes += 1

        # Save new ratings
        player_a.rating_mu = rating_a.mu
        player_a.rating_sigma = rating_a.sigma
        player_a.save()

        player_b.rating_mu = rating_b.mu
        player_b.rating_sigma = rating_b.sigma
        player_b.save()

        messages.success(request, _("Thanks for voting!"))
        return redirect('ranking', player_a.season)
