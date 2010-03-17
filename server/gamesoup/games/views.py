from django.contrib.admin.views.decorators import staff_member_required
from django.http import *
from django.shortcuts import *
from alphacabbage.django.helpers import get_pair_or_404
from alphacabbage.django.decorators import require_post
from gamesoup.games.models import *


@staff_member_required
def assemble_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'title': 'Assemble %s' % game.name.lower(),
        'game': game,
    }
    return render_to_response('admin/games/game-assemble.html', context)


@staff_member_required
@require_post
def instantiate_type(request, game_id, type_id):
    response = HttpResponse()
    return response


@staff_member_required
@require_post
def update_object_position(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    obj.x, obj.y = _get_numbers(request.POST, 'position')
    obj.save()
    return HttpResponse()


@staff_member_required
@require_post
def update_object_size(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    obj.width, obj.height = _get_numbers(request.POST, 'size')
    obj.save()
    return HttpResponse()


###############################################################################
# LOCAL HELPERS


def _get_numbers(post, name):
    return tuple(map(int, post[name].split(',')))
