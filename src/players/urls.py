from django.conf.urls import url

from players import views


urlpatterns = [
    url(r'^$', views.PlayerListView.as_view(), name='index'),
    url(r'^vote/$', views.PlayerVoteView.as_view(), name='vote'),
]
