from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.games.views',
    url(r'^game/(?P<game_id>\d+)/assemble/$', 'assemble_game', name='assemble_game'),
)
