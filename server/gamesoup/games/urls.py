from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.games.views',
    # Flow
    url(r'^game/(?P<game_id>\d+)/flow.(?P<format>png|svg)$', 'game_flow', name='game_flow'),

    # Code
    url(r'^game/(?P<game_id>\d+)/code/$', 'game_code', name='game_code'),
    
    # Search
    url(r'^search-requires/$', 'search_requires', name='search_requires'),
    url(r'^search-required-by/$', 'search_required_by', name='search_required_by'),
    url(r'^search-required-by-parameter/(?P<parameter_id>\d+)/$', 'search_required_by_parameter', name='search_required_by_parameter'),

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------

    # Assembler
    url(r'^game/(?P<game_id>\d+)/assemble/$', 'assemble_game', name='assemble_game'),
    url(r'^game/(?P<game_id>\d+)/refresh-assembler/$', 'refresh_assembler', name='refresh_assembler'),

    # Instantiating and configuring objects
    url(r'^game/(?P<game_id>\d+)/type/(?P<type_id>\d+)/instantiate/$', 'instantiate_type', name='instantiate_type'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-name/$', 'update_object_name', name='update_object_name'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-position/$', 'update_object_position', name='update_object_position'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/update-size/$', 'update_object_size', name='update_object_size'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/toggle-ownership/$', 'toggle_object_ownership', name='toggle_object_ownership'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/configure/$', 'object_configure', name='object_configure'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/delete/$', 'delete_object', name='delete_object'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/parameter/(?P<parameter_id>\d+)/save/$', 'save_parameter_binding', name='save_parameter_binding'),
    url(r'^game/(?P<game_id>\d+)/object/(?P<object_id>\d+)/parameter/(?P<parameter_id>\d+)/candidate-refs/$', 'candidate_refs', name='candidate_refs'),
)
