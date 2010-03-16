from django.http import *
from django.shortcuts import *
from gamesoup.games.models import *


def assemble_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'title': 'Assemble game',
        'game': game,
    }
    return render_to_response('admin/games/game-assemble.html', context)
