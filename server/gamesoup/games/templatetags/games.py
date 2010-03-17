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
