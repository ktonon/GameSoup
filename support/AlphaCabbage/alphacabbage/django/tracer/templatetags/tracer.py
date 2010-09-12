import re
from django import template
from django.template.loader import get_template
register = template.Library()


@register.simple_tag
def render_traced_object(obj):
    name = re.sub(r'(?<=[a-z])([A-Z][a-z]+)', r'_\1', obj.__class__.__name__).lower()
    t = get_template('tracer/_%s.html' % name)
    return t.render(template.Context({name: obj}))

@register.inclusion_tag('tracer/_args.html')
def render_args(mc):
    return {
        'args': mc._args, 
        'kwargs': mc._kwargs.items(),
        'join_comma': len(mc._args) > 0 and len(mc._kwargs) > 0 and ',' or '',
        }

@register.inclusion_tag('tracer/_object.html')
def render_object(obj):
    values = {}
    if hasattr(obj, '__dict__'):
        for key, value in obj.__dict__.items():
            if hasattr(value, '__repr__'):
                value = `value`
            elif hasattr(value, '__unicode__'):
                value = unicode(value)
            else:
                value = str(value)
            values[key] = value
        values = sorted(values.items(), cmp=lambda x, y: cmp(x[0], y[0]))
    return {
        'hash': str(id(obj)),
        'shortHash': str(id(obj))[-3:],
        'className': obj.__class__.__name__,
        'fullClassName': str(obj.__class__),
        'str': str(obj),
        'unicode': unicode(obj),
        'repr': `obj`,
        'values': values,
    }

@register.inclusion_tag('tracer/_traceback.html')
def render_traceback(mc):
    return {
        'method_call': mc,
        'stacks': mc._tb,
    }
