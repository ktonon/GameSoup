import json
from django import template


register = template.Library()


@register.inclusion_tag('admin/games/assembler/objects.html')
def objects(game):
    return {
        'game': game,
        'objects': game.object_set.all().order_by('type'),
    }


@register.inclusion_tag('admin/games/assembler/canvas.html')
def canvas(game):
    return {
        'game': game,
        'objects': game.object_set.filter(type__visible=True),
    }


@register.simple_tag
def binding(object, parameter):
    from gamesoup.games.models import Binding
    try:
        return Binding.objects.get(instance=object, parameter=parameter)
    except Binding.DoesNotExist:
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
        w = 'gamesoup.games.objects[%d]._%s = ' % (object.id, binding.parameter.name)
        if binding.parameter.interface.is_built_in:
            w += json.dumps(_built_in[binding.parameter.interface.name](binding.built_in_argument))
        else:
            w += 'gamesoup.games.objects[%d]' % binding.object_argument.id
        result += '%s;\n' % w
    return result


_built_in = {
    'Integer': int,
    'Float': float,
    'String': str,
    'Boolean': bool,
}
