from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from nba_py.constants import CURRENT_SEASON


urlpatterns = [
    # Redirect to current season ranking view
    url(r'^$',
        RedirectView.as_view(pattern_name='ranking'),
        {'season': CURRENT_SEASON},
        name='index'),

    # Main application part
    url(r'', include('players.urls')),

    # Django Admin
    url(r'^django_admin/', include(admin.site.urls)),
]


# Serve static files on runserver
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
