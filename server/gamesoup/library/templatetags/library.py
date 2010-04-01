from django import template
from django.utils.safestring import mark_safe


register = template.Library()


###############################################################################
# For producing boilerplate code


@register.simple_tag
def code_doc(component, count=0):
    '''
    Format the description field of a component (either method or type).
    
    Usage::
    
        {% code_doc method %}
    
    produces::
    
         * The description...
         * ...
         * ...        
    '''
    if not component.description: return ''
    prefix = '\n%s * ' % ('    ' * count)
    return prefix + component.description.replace('\n', prefix)


@register.simple_tag
def engine_hook(parsed, name):
    '''
    Access the body of an engine-hook method.
    
    Usage::
    
        {% engine_hook parsed method_name %}
    
    where parsed is an instance of gamesoup.library.code.TypeCode.
    '''
    return mark_safe(parsed.engine_hook(name))


@register.simple_tag
def interface_method(parsed, name):
    '''
    Access the body of the type implementation of an interface method.
    
    Usage::
    
        {% interface_method parsed method_name %}
    
    where parsed is an instance of gamesoup.library.code.TypeCode.
    '''
    return mark_safe(parsed.interface_method(name))


@register.simple_tag
def method_signature_for_type(type, method):
    return method.get_signature(as_implemented_by_type=type)


###############################################################################
# FOR LOADING OBJECTS INTO admin/change_form.html TEMPLATES


class GetObjectNode(template.Node):
    def __init__(self, id_varname, varname, model):
        self.id_var = template.Variable(id_varname)
        self.varname = varname
        self.model = model
    def render(self, context):
        try:
            id = self.id_var.resolve(context)
            context[self.varname] = self.model.objects.get(pk=id)
        except Exception:
            pass
        return u''

def get_object(parser, token, model):
    try:
        tag_name, _for, id, _as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r for id_varname as varname" % token.contents.split()[0]
    return GetObjectNode(id, varname, model)

@register.tag
def get_method(parser, token):
    '''
    Load a Method object into the context given a primary key.
    
    Usage::
    
        {% get_method for object_id as varname %}
    
    after this call *varname* will contain the Method object.
    '''
    from gamesoup.library.models import Method
    return get_object(parser, token, Method)

@register.tag
def get_interface(parser, token):
    '''
    Load a Interface object into the context given a primary key.
    
    Usage::
    
        {% get_interface for object_id as varname %}
    
    after this call *varname* will contain the Interface object.
    '''
    from gamesoup.library.models import Interface
    return get_object(parser, token, Interface)
