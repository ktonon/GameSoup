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
    
    bindings = TypeParameterBinding.objects.filter(instance__game=game, parameter__is_built_in=False)
    for ref in bindings.filter(parameter__is_factory=False):
        e = g.add_edge(nodes[ref.instance.id], nodes[ref.object_argument.id])
        e.label = ref.parameter.name
        e.color = 'gray'
        e.fontcolor = 'blue'
        e.labelfloat = True
        e.fontsize = 14
        e.len = 3
    for factory in bindings.filter(parameter__is_factory=True):
        e = g.add_edge(nodes[factory.instance.id], nodes['type_%d' % factory.type_argument.id])
        e.label = factory.parameter.name
        e.color = 'gray'
        e.fontcolor = 'gray'
        e.labelfloat = True
        e.fontsize = 14
        e.len = 3

    # Danglers
    for param in TypeParameter.objects.filter(of_type__instances__game=game, is_built_in=False).distinct():
        if param.bindings.filter(instance__game=game).count() == 0:
            for obj in Object.objects.filter(game=game, type__parameters=param).distinct():
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
# In these methods we use "or [0]" because of the way the type ids are
# used by the javascript client. Eventually, these types are used in a query
# to a django change list view that takes the form "id__in=%s" % ','.join(type_ids)
# If we use an empty list, this results in an invalid query, and django by default
# will show all types, which is not what we want. If we use [0] instead,
# then the query reads "id__in=0", which will not return any types.

@staff_member_required
@require_post
def search_requires(request):
    obj_ids = map(int, filter(bool, request.POST['object_ids'].split(',')))
    if obj_ids:
        qs = Type.objects.all()
        for obj_id in obj_ids:
            obj = Object.objects.get(pk=obj_id)
            qs = qs.filter(parameters__interfaces__implemented_by=obj.type)
        type_ids = [t.id for t in qs]
    else:
        type_ids = []
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(type_ids or [0])) # See comment above
    return response


@staff_member_required
@require_post
def search_required_by(request):
    from django.db.models import Q
    obj_ids = map(int, filter(bool, request.POST['object_ids'].split(',')))
    if obj_ids:
        type_ids = set()
        for obj_id in obj_ids:
            obj = Object.objects.get(pk=obj_id)
            for param in obj.type.parameters.all():
                qs = Type.objects.all()
                expr = Expr.parse(param.expression_text)
                for interface in Interface.objects.for_expr(expr):
                    qs = qs.filter(implements=interface)
                type_ids |= set([t.id for t in qs])
        type_ids = list(type_ids)
    else:
        type_ids = []
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(type_ids or [0])) # See comment above
    return response


@staff_member_required
def search_required_by_parameter(request, parameter_id):
    param = get_object_or_404(TypeParameter, pk=parameter_id)
    qs = Type.objects.all()
    expr = Expr.parse(param.expression_text)
    for interface in Interface.objects.for_expr(expr):
        qs = qs.filter(implements=interface)
    if param.is_factory:
        qs = qs.filter(parameters__isnull=True).distinct()
    type_ids = [t.id for t in qs]
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
    context = {
        'title': 'Configure %s' % obj.type.name,
        'obj': obj,
        'built_ins': obj.type.parameters.filter(is_built_in=True).order_by('name'),
        'refs': obj.type.parameters.filter(is_built_in=False, is_factory=False).order_by('name'),
        'factories': obj.type.parameters.filter(is_built_in=False, is_factory=True).order_by('name'),
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
    except TypeParameter.DoesNotExist:
        raise Http404()
    value = {}
    x = request.POST['value']
    try:
        binding = obj.parameter_bindings.get(parameter=param)
    except TypeParameterBinding.DoesNotExist:
        binding = TypeParameterBinding(instance=obj, parameter=param)
    data = {}
    if param.is_built_in:
        binding.built_in_argument = x
        data['value'] = x
    else:
        if param.is_factory:
            binding.type_argument = Type.objects.get(pk=x)
            data['value'] = binding.type_argument.name
        else:
            binding.object_argument = Object.objects.get(pk=x)
            data['value'] = binding.object_argument.name
    binding.save()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(data))
    return response
    

@staff_member_required
def candidate_refs(request, game_id, object_id, parameter_id):
    game, obj = get_pair_or_404(Game, 'object_set', game_id, object_id)
    try:
        param = obj.type.parameters.get(pk=parameter_id)
    except TypeParameter.DoesNotExist:
        raise Http404()
    qs = game.object_set.all()
    expr = Expr.parse(param.expression_text)
    for interface in Interface.objects.for_expr(expr):
        qs = qs.filter(type__implements=interface)
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps(['object-%d' % obj.id for obj in qs]))
    return response


###############################################################################
# LOCAL HELPERS


def _get_numbers(post, name):
    return tuple(map(int, post[name].split(',')))
