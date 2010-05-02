import json
from django import template
from gamesoup.expressions.syntax import Expr
from gamesoup.library.templatetags.library import get_object as _get_object


register = template.Library()


@register.inclusion_tag('admin/games/assembler/objects.html')
def assembler_objects(game):
    '''
    Render to *admin/games/assembler/objects.html*
    
    Usage::

        {% assembler_objects game %}
    '''
    return {
        'game': game,
        'objects': game.object_set.all(),
    }


@register.inclusion_tag('admin/games/assembler/canvas.html')
def assembler_canvas(game):
    '''
    Render to *admin/games/assembler/canvas.html*
    
    Usage::

        {% assembler_canvas game %}
    '''
    return {
        'game': game,
        'objects': game.object_set.filter(type__visible=True),
    }


@register.inclusion_tag('admin/games/assembler/flow.html')
def assembler_flow(game):
    '''
    Render to *admin/games/assembler/flow.html*
    
    Usage::

        {% assembler_flow game %}
    '''
    return {
        'game': game,
    }


@register.simple_tag
def set_object_parameters(object):
    '''
    Produce JavaScript to initialize an object parameter with an argument.
    
    Usage::
    
        {% set_object_parameter object %}
    '''
    result = ''
    for binding in object.bindings.all():
        w = 'gamesoup.matches.objects[%d]._%s = ' % (object.id, binding.parameter.name)
        if binding.parameter.is_built_in:
            w += json.dumps(_built_in[`binding.parameter.expr`](binding.built_in_argument))
        else:
            if binding.parameter.is_factory:
                w += 'gamesoup.library.types.%s' % binding.type_argument.name
            else:
                w += 'gamesoup.matches.objects[%d]' % binding.object_argument.id
        result += '%s;\n' % w
    return result


_built_in = {
    'Integer!': int,
    'Float!': float,
    'String!': str,
    'Boolean!': bool,
}


###############################################################################
# FOR LOADING OBJECTS INTO admin/change_form.html TEMPLATES


@register.tag
def get_game(parser, token):
    '''
    Load a Game object into the context given a primary key.

    Usage::

        {% get_interface for object_id as varname %}

    after this call *varname* will contain the Game object.
    '''
    from gamesoup.games.models import Game
    return _get_object(parser, token, Game)


@register.tag
def get_object(parser, token):
    '''
    Load an Object object into the context given a primary key.

    Usage::

        {% get_interface for object_id as varname %}

    after this call *varname* will contain the Object object.
    '''
    from gamesoup.games.models import Object
    return _get_object(parser, token, Object)
