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
