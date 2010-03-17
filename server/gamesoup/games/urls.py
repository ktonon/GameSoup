from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.games.views',
    url(r'^game/(?P<game_id>\d+)/assemble/$', 'assemble_game', name='assemble_game'),
    url(r'^game/(?P<game_id>\d+)/type/(?P<type_id>\d+)/instantiate/$', 'instantiate_type', name='instantiate_type'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-position/$', 'update_object_position', name='update_object_position'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-size/$', 'update_object_size', name='update_object_size'),
)
