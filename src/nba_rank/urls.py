from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from players.views import PlayerListView, PlayerVoteView


urlpatterns = [
    url(r'^$', PlayerListView.as_view(), name='index'),
    url(r'^vote/$', PlayerVoteView.as_view(), name='vote'),

    # Django Admin
    url(r'^django_admin/', include(admin.site.urls)),
]


# Serve static files on runserver
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
