from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.matches.views',
    url(r'^match/(?P<match_id>\d+)/play/$', 'play_match', name='play_match'),
)
