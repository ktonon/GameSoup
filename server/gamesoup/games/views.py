import json
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import *
from django.shortcuts import *
from django.template import Context
from django.template.loader import get_template
from alphacabbage.django.helpers import get_pair_or_404
from alphacabbage.django.decorators import require_post
from gamesoup.games.models import *
from gamesoup.expressions.syntax import Expr


###############################################################################
# FLOW


@staff_member_required
def game_flow(request, game_id, format):
    import yapgvb, os.path
    game = get_object_or_404(Game, pk=game_id)
    # subprocess.call(['dot', '-T', 'png'], )
    response = HttpResponse(mimetype=format == 'svg' and 'image/svg+xml' or 'image/png')
    g = yapgvb.Digraph('Flow')
    # g.rankdir = 'LR'
    nodes = {}
    for obj in game.object_set.all():
        n = g.add_node(obj.id, label=str(obj).replace('"', '\\"'))
        n.width = len(str(obj)) / 10
        n.style = 'filled'
        if obj.type.visible:
            n.shape = 'box'
        if obj.type.has_state:
            if obj.per_player:
                n.fillcolor = '#6699cc'
            else:
                n.fillcolor = '#99ccff'
        nodes[obj.id] = n
    for type in Type.objects.filter(bound_to__instance__game=game).distinct():
        n = g.add_node('type_%d' % type.id, label=str(type).replace('"', '\\"'))
        n.width = len(str(type)) / 10
        n.style = 'filled'
        n.fillcolor = 'black'
        n.fontcolor = 'white'
        nodes['type_%d' % type.id] = n
    
    bindings = ObjectParameterBinding.objects.filter(instance__game=game)
    for ref in bindings.filter(parameter__type_parameter__is_factory=False):
        if ref.parameter.is_built_in: continue
        e = g.add_edge(nodes[ref.instance.id], nodes[ref.object_argument.id])
        e.label = ref.parameter.name
        e.color = 'gray'
        e.fontcolor = 'blue'
        e.labelfloat = True
        e.fontsize = 14
        e.len = 3
    for factory in bindings.filter(parameter__type_parameter__is_factory=True):
        if factory.parameter.is_built_in: continue
        e = g.add_edge(nodes[factory.instance.id], nodes['type_%d' % factory.type_argument.id])
        e.label = ''#factory.parameter.type_parameter.of_type.name
        e.color = 'gray'
        e.fontcolor = 'gray'
        e.labelfloat = True
        e.fontsize = 14
        e.len = 3

    # Danglers
    for param in ObjectParameter.objects.filter(type_parameter__of_type__instances__game=game).distinct():
        if param.is_built_in: continue
        if param.binding is None:
            obj = param.of_object
            n = g.add_node('missing_param_%d_%d' % (obj.id, param.id), label='')
            n.color = 'white'
            e = g.add_edge(nodes[obj.id], n)
            e.color = 'red'
            e.fontcolor = 'red'
            e.label = param.name
            
    g.layout(yapgvb.engines.dot)
    scratch_path = os.path.join(settings.MEDIA_ROOT, 'flow-scratch', 'game-%d.%s' % (game.id, format))
    g.render(scratch_path)
    scratch = open(scratch_path)
    response.write(scratch.read())
    return response


###############################################################################
# CODE


@staff_member_required
def game_code(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    t = get_template('games/game/code.js')
    query = Q(instances__game=game) | Q(bound_to__instance__game=game)
    types = Type.objects.filter(query).distinct().order_by('name')
    c = Context({
        'game': game,
        'types': types,
        'objects': game.object_set.all(),
        'stateful_objects': game.object_set.filter(type__has_state=True),
        'visible_objects': game.object_set.filter(type__visible=True),
    })
    response = HttpResponse(mimetype='text/javascript')
    response.write(t.render(c))
    return response


###############################################################################
# SEARCH
#
# In these methods we use "or [0]" because of the way the type ids are used by
# the javascript client. Eventually, these types are used in a query to a
# django change list view that takes the form "id__in=%s" % ','.join(type_ids)
# If we use an empty list, this results in an invalid query, and django by
# default will show all types, which is not what we want. If we use [0]
# instead, then the query reads "id__in=0", which will not return any types.

@staff_member_required
@require_post
def search_requires(request):
    obj_ids = map(int, filter(bool, request.POST['object_ids'].split(',')))
    if obj_ids:
        qs = Type.objects.all()
        for obj_id in obj_ids:
            obj = Object.objects.get(pk=obj_id)
            qs = qs.filter(parameters___interfaces__implemented_by=obj.type).distinct()
        def d(t):
            params = t.parameters.filter(_is_ref=True)
            n = params.count()
            params2 = params.exclude(_interfaces__implemented_by__instances__id__in=obj_ids).distinct()
            return params2.count() <= n - len(obj_ids)
        type_ids = [t.id for t in qs if d(t)]
    else:
        type_ids = []
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(type_ids or [0])) # See comment above
    return response


@staff_member_required
def search_required_by_parameter(request, parameter_id):
    param = get_object_or_404(ObjectParameter, pk=parameter_id)
    type_ids = [t.id for t in param.candidate_types]
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(type_ids or [0])) # See comment above
    return response
    

###############################################################################
# ASSEMBLER


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
    

###############################################################################
# INSTANTIATING AND CONFIGURING OBJECTS


@staff_member_required
@require_post
def instantiate_type(request, game_id, type_id):
    '''
    Instantiate a new object and returns {objectID: obj.id} in a JSON response.
    '''
    game = get_object_or_404(Game, pk=game_id)
    type = get_object_or_404(Type, pk=type_id)
    obj = game.object_set.create(type=type)
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps({'objectID': obj.id, 'typeName': type.name}))
    return response


@staff_member_required
@require_post
def update_object_name(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    obj.name = request.POST['name']
    obj.save()
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
@require_post
def toggle_object_ownership(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    obj.per_player = not obj.per_player
    obj.save()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps({'ownership': obj.per_player and 'player' or 'game'}))
    return response


@staff_member_required
def object_configure(request, game_id, object_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    params = obj.parameters.all()
    def f(attr):
        return filter(lambda p: getattr(p, attr), params)
    context = {
        'title': 'Configure %s' % obj.type.name,
        'obj': obj,
        'parameters': params,
        'built_ins': f('is_built_in'),
        'refs': f('is_ref'),
        'factories': f('is_factory'),
        'nothing_to_configure': obj.parameters.count() == 0,
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
        param = obj.parameters.get(pk=parameter_id)
    except ObjectParameter.DoesNotExist:
        raise Http404()
    value = param.bind(request.POST['value'])
    data = {'value': unicode(value)}
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(data))
    return response
    

@staff_member_required
def candidate_refs(request, game_id, object_id, parameter_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    try:
        param = obj.parameters.get(pk=parameter_id)
    except ObjectParameter.DoesNotExist:
        raise Http404()    
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(['object-%d' % obj.id for obj in param.candidate_objects]))
    return response


###############################################################################
# LOCAL HELPERS


def _get_numbers(post, name):
    return tuple(map(int, post[name].split(',')))
