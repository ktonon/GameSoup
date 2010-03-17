from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.games.views',
    url(r'^game/(?P<game_id>\d+)/assemble/$', 'assemble_game', name='assemble_game'),
    url(r'^game/(?P<game_id>\d+)/refresh-assembler/$', 'refresh_assembler', name='refresh_assembler'),
    url(r'^game/(?P<game_id>\d+)/type/(?P<type_id>\d+)/instantiate/$', 'instantiate_type', name='instantiate_type'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-position/$', 'update_object_position', name='update_object_position'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-size/$', 'update_object_size', name='update_object_size'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/configure/$', 'object_configure', name='object_configure'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/delete/$', 'delete_object', name='delete_object'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/parameter/(?P<parameter_id>\d+)/save/$', 'save_parameter_binding', name='save_parameter_binding'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/parameter/(?P<parameter_id>\d+)/candidate-refs/$', 'candidate_refs', name='candidate_refs'),
)
