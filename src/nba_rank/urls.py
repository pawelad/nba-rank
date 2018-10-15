"""
NBA Rank main URL config.
"""
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin

from nba_py.constants import CURRENT_SEASON


urlpatterns = [
    # Redirect to current season ranking view
    path(
        '',
        RedirectView.as_view(pattern_name='ranking'),
        kwargs={'season': CURRENT_SEASON},
        name='index'
    ),

    path('', include('players.urls')),

    # Django Admin
    path('django_admin/', admin.site.urls),
]
