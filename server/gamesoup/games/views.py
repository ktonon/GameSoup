import json
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
def refresh_assembler(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'game': game,
    }
    return render_to_response('admin/games/assembler/refresh.html', context)
    
    
@staff_member_required
@require_post
def instantiate_type(request, game_id, type_id):
    game = get_object_or_404(Game, pk=game_id)
    type = get_object_or_404(Type, pk=type_id)
    game.object_set.create(type=type)
    return HttpResponse()


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


@staff_member_required
def object_configure(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    context = {
        'title': 'Configure %s' % obj.type.name,
        'obj': obj,
        'built_ins': obj.type.parameters.filter(interface__is_built_in=True).order_by('name'),
        'refs': obj.type.parameters.filter(interface__is_built_in=False).order_by('name'),
        'nothing_to_configure': obj.type.parameters.count() == 0,
    }
    return render_to_response('admin/games/object-configure.html', context)


@staff_member_required
@require_post
def delete_object(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    obj.delete()
    return HttpResponse()


@staff_member_required
@require_post
def save_parameter_binding(request, game_id, object_id, parameter_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    try:
        param = obj.type.parameters.get(pk=parameter_id)
    except Variable.DoesNotExist:
        raise Http404()
    value = {}
    x = request.POST['value']
    if param.interface.is_built_in:
        value['built_in_argument'] = x
    else:
        value['object_argument'] = x
    try:
        binding = obj.parameter_bindings.get(parameter=param)
    except Binding.DoesNotExist:
        binding = Binding(instance=obj, parameter=param)
    if param.interface.is_built_in:
        binding.built_in_argument = x
    else:
        binding.object_argument = Object.objects.get(pk=x)
    binding.save()
    return HttpResponse()


@staff_member_required
def candidate_refs(request, game_id, object_id, parameter_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    try:
        param = obj.type.parameters.get(pk=parameter_id)
    except Variable.DoesNotExist:
        raise Http404()
    qs = Object.objects.filter(type__implements=param.interface)
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(['object-%d' % obj.id for obj in qs]))
    return response


###############################################################################
# LOCAL HELPERS


def _get_numbers(post, name):
    return tuple(map(int, post[name].split(',')))
