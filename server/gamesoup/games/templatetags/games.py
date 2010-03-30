import json
from django import template


register = template.Library()


@register.inclusion_tag('admin/games/assembler/objects.html')
def objects(game):
    return {
        'game': game,
        'objects': game.object_set.all(),
    }


@register.inclusion_tag('admin/games/assembler/canvas.html')
def canvas(game):
    return {
        'game': game,
        'objects': game.object_set.filter(type__visible=True),
    }


@register.inclusion_tag('admin/games/assembler/flow.html')
def flow(game):
    return {
        'game': game,
    }


@register.simple_tag
def binding(object, parameter):
    from gamesoup.games.models import TypeParameterBinding
    try:
        return TypeParameterBinding.objects.get(instance=object, parameter=parameter)
    except TypeParameterBinding.DoesNotExist:
        return ''


@register.simple_tag
def satisfiable_parameter(object, parameter):
    from gamesoup.games.models import Object
    sat = Object.objects.filter(game=object.game, type__implements=parameter.interface).count() > 0
    return not sat and 'unsatisfiable' or ''


@register.simple_tag
def set_object_parameters(object):
    result = ''
    for binding in object.parameter_bindings.all():
        w = 'gamesoup.matches.objects[%d]._%s = ' % (object.id, binding.parameter.name)
        if binding.parameter.interface.is_built_in:
            w += json.dumps(_built_in[binding.parameter.interface.name](binding.built_in_argument))
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
    Get the parameter binding for the given object.
        {%% parameter_binding obj param as binding %%}
    '''
    try:
        tag_name, obj_varname, param_varname, _as, binding_varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "Invalid usage"
    return ParameterBindingNode(obj_varname, param_varname, binding_varname)