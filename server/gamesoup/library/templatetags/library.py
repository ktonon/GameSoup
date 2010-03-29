from django import template
from django.utils.safestring import mark_safe
from gamesoup.library.parsers import parse_method_signature
from gamesoup.library.templation import InterfaceExpression


register = template.Library()


@register.simple_tag
def code_doc(component, count=0):
    if not component.description: return ''
    prefix = '\n%s * ' % ('    ' * count)
    return prefix + component.description.replace('\n', prefix)


@register.simple_tag
def method_signature_doc(method):
    context = {
        'Item': 'Foo'
        }
    
    def resolve(w):
        exp = InterfaceExpression(w)
        return `exp` % context
    
    d = parse_method_signature(method.signature)
    w = ''
    if d['returned']:
        w += resolve(d['returned'].interface_name) + ' '
    w += '%s(' % d['name']
    x = []
    for param in d['parameters']:
        x.append('%s %s' % (resolve(param.interface_name), param.name))
    w += ', '.join(x)
    w += ')'
    return w


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
