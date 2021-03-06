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
def method_signature_for_type(type, method, escaped=None):
    w = method.get_signature(as_implemented_by_type=type)
    if escaped:
        w = w.replace('<', '&lt;').replace('>', '&gt;')
    return w


class GetStrongestExpressionForInterfaceNode(template.Node):
    def __init__(self, type_varname, interface_varname, varname):
        self.type_var = template.Variable(type_varname)
        self.interface_var = template.Variable(interface_varname)
        self.varname = varname
    def render(self, context):
        type = self.type_var.resolve(context)
        interface = self.interface_var.resolve(context)
        context[self.varname] = interface.get_expr(as_implemented_by_type=type)
        return u''


@register.tag
def get_expr_for_interface(parser, token):
    '''
    Usage::
    
        {% get_expr_for_interface interface of type as varname %}
    '''
    try:
        tag_name, interface_varname, _of, type_varname, _as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "See doc for %r" % token.contents.split()[0]
    return GetStrongestExpressionForInterfaceNode(type_varname, interface_varname, varname)


class GetStrongestExpressionForTypeNode(template.Node):
    def __init__(self, type_varname, object_varname, varname):
        self.type_var = template.Variable(type_varname)
        self.object_var = template.Variable(object_varname)
        self.varname = varname
    def render(self, context):
        obj = self.object_var.resolve(context)
        type = self.type_var.resolve(context)
        context[self.varname] = type.get_expr(as_instantiated_by_object=obj)
        return u''


@register.tag
def get_expr_for_type(parser, token):
    '''
    Usage::

        {% get_expr_for_interface interface of type as varname %}
    '''
    try:
        tag_name, type_varname, _of, object_varname, _as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "See doc for %r" % token.contents.split()[0]
    return GetStrongestExpressionForTypeNode(type_varname, object_varname, varname)


@register.filter
def expr_with_links(expr):
    return expr.replace('<', '&lt;').replace('>', '&gt;')
    
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


@register.tag
def get_type(parser, token):
    '''
    Load a Type object into the context given a primary key.

    Usage::

        {% get_type for object_id as varname %}

    after this call *varname* will contain the Type object.
    '''
    from gamesoup.library.models import Type
    return get_object(parser, token, Type)


class MethodsForTypeNode(template.Node):
    def __init__(self, type_varname, methods_varname):
        self.type_var = template.Variable(type_varname)
        self.methods_varname = methods_varname
    def render(self, context):
        from gamesoup.library.models import Method
        type = self.type_var.resolve(context)
        qs = Method.objects.filter(interface__implemented_by=type)
        context[self.methods_varname] = qs
        return u''


@register.tag
def methods_for_type(parser, token):
    '''
    Load the methods of a given type into the context.

    Usage::

        {% methods_for_type type as varname %}
    '''
    try:
        tag_name, type_varname, _as, methods_varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "See usage for %r" % token.contents.split()[0]
    return MethodsForTypeNode(type_varname, methods_varname)
