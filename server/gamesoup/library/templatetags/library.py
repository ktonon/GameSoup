from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def code_doc(component, count=0):
    if not component.description: return ''
    prefix = '\n%s * ' % ('    ' * count)
    return prefix + component.description.replace('\n', prefix)


@register.simple_tag
def built_in(param):
    t = "this._node.down('.argument[name=%s]').getAttribute('value')" % param.name
    x = {
        'Integer': 'new Number(%s)',
        'Float': 'new Number(%s)',
        'String': '%s',
        'Boolean': '%s == "true"',
    }
    return x[param.interface.name] % t


@register.filter
def engine_hook(parsed, name):
    return mark_safe(parsed.engine_hook(name))


@register.simple_tag
def interface_method(parsed, name):
    return mark_safe(parsed.interface_method(name))
