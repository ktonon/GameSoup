from django.contrib.admin.views.decorators import staff_member_required
from django.http import *
from django.shortcuts import *
from gamesoup.matches.models import *


@staff_member_required
def play_match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    context = {
        'title': 'Play %s' % match,
        'match': match,
        'game': match.game,
    }
    return render_to_response('admin/matches/match/play.html', context)
