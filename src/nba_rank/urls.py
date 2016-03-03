from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='nba_rank/index.html'), name='index'),

    # Django Admin
    url(r'^django_admin/', include(admin.site.urls)),
]


# Serve static files on runserver
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
