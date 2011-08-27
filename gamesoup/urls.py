from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # User authentication
    url(r'^login/$', 'gamesoup.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    
    # Admin site:
    (r'^admin/games/', include('gamesoup.games.urls', namespace='games', app_name='games')),
    (r'^admin/library/', include('gamesoup.library.urls', namespace='library', app_name='library')),
    (r'^admin/matches/', include('gamesoup.matches.urls', namespace='matches', app_name='matches')),
    (r'^admin/expressions/', include('gamesoup.expressions.urls', namespace='expressions', app_name='expressions')),
    (r'^admin/graphs/', include('alphacabbage.django.graphs.urls', namespace='graphs', app_name='graphs')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
