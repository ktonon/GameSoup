import yapgvb, datetime
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import *
from django.template import Context
from django.template.loader import get_template
from gamesoup.expressions.models import *
from gamesoup.expressions.forms import *


_mimetype = {
    'png': 'image/png',
    'svg': 'image/svg+xml',
}

@staff_member_required
def index(request):
    context = {
        'title': 'Expressions',
    }
    return render_to_response('admin/expressions/app_index.html', context)


@staff_member_required
def render(request, type):
    format = 'png'
    try:
        render_func = __import__('gamesoup.expressions.visualize.%s' % type, {}, {}, ['render']).render
    except ImportError:
        raise Http404()
    if request.method == 'POST':
        form = ExpressionForm(request.POST)
        if form.is_valid():
            w = form.cleaned_data['expr']
            request.session['last_expression'] = w
            # Render it
            g = yapgvb.Digraph(type.capitalize())
            g.layout(yapgvb.engines.dot)
            request.session['last_rendering'] = render_func(w, g)
            scratch_path = os.path.join(settings.MEDIA_ROOT, 'graphs-scratch/rendered-expressions', '%s.%s' % (type, format))
            g.render(scratch_path)
            return HttpResponseRedirect('.')
    else:
        form = ExpressionForm(data={'expr': request.session.get('last_expression', '')})
    context = {
        'title': type.capitalize(),
        'form': form,
        'type': type,
        'format': format,
        'time': datetime.datetime.now(),
        'last_expression': request.session.get('last_expression', 'Cannot remember'),
        'last_rendering': request.session.get('last_rendering', 'Cannot remember'),
    }
    return render_to_response('admin/expressions/render.html', context)
