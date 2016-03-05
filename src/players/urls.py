from django.conf.urls import url

from players import views


urlpatterns = [
    url(r'^(?P<season>\d{4}-\d{2})/$',
        views.PlayerListView.as_view(), name='ranking'),
    url(r'^(?P<season>\d{4}-\d{2})/vote/$',
        views.PlayerVoteModalView.as_view(), name='vote_modal'),
    url(r'^vote_save/(?P<signed_data>[\w:=_-]+)/$',
        views.PlayerVoteSaveView.as_view(), name='vote_save'),
]
