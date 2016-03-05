from django.conf.urls import url

from players import views


urlpatterns = [
    url(r'^$', views.PlayerListView.as_view(), name='index'),
    url(r'^vote/$', views.PlayerVoteModalView.as_view(), name='vote_modal'),
    url(r'^vote/(?P<signed_data>[\w:=_-]+)/$',
        views.PlayerVoteSaveView.as_view(), name='vote_save'),
]
