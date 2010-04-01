import json
from django import template
from gamesoup.library.expressions.semantics import InterfaceExpression
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
def satisfiable_parameter(object, parameter):
    '''
    If a parameter is unsatisfiable, returns the word "unsatisfiable".
    
    Usage::
        
        {% satisfiable_parameter object parameter %}
    
    This is meant to be used to produce a CSS class name.
    '''
    from gamesoup.games.models import Object
    qs = Object.objects.filter(game=object.game)
    expr = InterfaceExpression.parse(parameter.expression)
    for interface in expr.interfaces:
        qs = qs.filter(type__implements=interface)
    sat = qs.count() > 0
    return not sat and 'unsatisfiable' or ''


@register.simple_tag
def set_object_parameters(object):
    '''
    Produce JavaScript to initialize an object parameter with an argument.
    
    Usage::
    
        {% set_object_parameter object %}
    '''
    result = ''
    for binding in object.parameter_bindings.all():
        w = 'gamesoup.matches.objects[%d]._%s = ' % (object.id, binding.parameter.name)
        if binding.parameter.is_built_in:
            w += json.dumps(_built_in[binding.parameter.interface.name](binding.built_in_argument))
        else:
            if binding.parameter.is_factory:
                w += 'gamesoup.library.types.%s' % binding.type_argument.name
            else:
                w += 'gamesoup.matches.objects[%d]' % binding.object_argument.id
        result += '%s;\n' % w
    return result


_built_in = {
    'Integer': int,
    'Float': float,
    'String': str,
    'Boolean': bool,
}

class ParameterBindingNode(template.Node):
    def __init__(self, obj_varname, param_varname, binding_varname):
        self.obj_var = template.Variable(obj_varname)
        self.param_var = template.Variable(param_varname)
        self.binding_varname = binding_varname
    def render(self, context):
        from gamesoup.games.models import TypeParameterBinding
        obj = self.obj_var.resolve(context)
        param = self.param_var.resolve(context)
        try:
            binding = TypeParameterBinding.objects.get(instance=obj, parameter=param)
        except TypeParameterBinding.DoesNotExist:
            binding = None
        context[self.binding_varname] = binding
        return u''

@register.tag
def parameter_binding(parser, token):
    '''
    For a given object and parameter load the binding into the context.
    
    Usage::
    
        {% parameter_binding obj param as binding %}
    
    After this call, the variable *binding* with contain the TypeParameterBinding object.
    '''
    try:
        tag_name, obj_varname, param_varname, _as, binding_varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "Invalid usage"
    return ParameterBindingNode(obj_varname, param_varname, binding_varname)


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
