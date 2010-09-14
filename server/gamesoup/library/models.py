'''
Stores the components from which games are made. The most important of these are types.
'''


import re
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import *
from django.template import Context
from django.template.loader import get_template
from alphacabbage.django.choices import *
from gamesoup.library.errors import *
from gamesoup.library.fields import *
from gamesoup.library.managers import *
from gamesoup.library.code import TypeCode
from gamesoup.expressions.syntax import Expr


class Method(models.Model):
    '''
    Method signature.
    '''
    interface = models.ForeignKey('Interface', related_name='methods')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    return_expression_text = ExprField('Return', default='', blank=True)

    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return self.signature
    
    def get_signature(self, as_implemented_by_type=None):
        type = as_implemented_by_type
        bc = type and type.binding_context or None
        c = type and type.context or None
        def resolve(expr):
            if bc:
                expr = expr % bc
            if c:
                expr = expr % c
            return expr
        # resolve = lambda expr: type and ((expr % bc) % c) or expr
        w = u'%s(%s)' % (self.name, ' ; '.join([
            '%s : %r' % (p.name, resolve(p.expr))
            for p in self.parameters.all()]))            
        ret = Expr.parse(self.return_expression_text)
        if ret: w += ' : %s' % resolve(ret)
        return w
    get_signature.short_description = 'Signature'
    signature = property(get_signature)
    
    @classmethod
    def reset(cls):
        for method in cls.objects.all():
            method.save()


class Interface(models.Model):
    '''
    A set of public methods available on instances of an object.
    Interfaces can be abstracted using template parameters.
    '''
    name = IdentifierField(help_text='A unique name. Should be specified using MixedCase with no spaces.')
    description = models.TextField(blank=True, help_text='This will serve as a human-readable, searchable account of this interface. Make this very detailed, because this will be the primary description of this interface for game designers.')
    is_built_in = models.BooleanField(default=False, help_text="Built-in interfaces are provided by the underlying language (JavaScript) or library (Prototype) and do not require a Type to be implemented.")

    objects = InterfaceManager()

    #--------------------------------------------------------------------------
    # Dynamic
    
    expr = property(lambda self: Expr.parse('%s<%s>' % (self.name, self.context)))
    context = property(lambda self: self.template_parameters.get_context())
    
    #--------------------------------------------------------------------------
    # Representation

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        qs = self.template_parameters.all()
        return self.name + (qs and u'<%s>' % ','.join([u'%s=%s' % (tp.name, tp.expression_text) for tp in qs]) or u'')

    def implemented_by_short(self):
        return ', '.join([type.name for type in self.implemented_by.all()])
    implemented_by_short.short_description = 'Implemented by'

    def doc_link(self):
        return '<a href="%s">%s</a>' % (
            reverse('library:interface_documentation', args=[self.id]),
            '<br/>'.join([m.signature for m in self.methods.all()])
        )
    doc_link.allow_tags = True
    doc_link.short_description = 'Documentation'

    
class Type(models.Model):
    '''
    An instantiable type.
    Types can implement multiple interfaces.
    '''
    name = IdentifierField()
    title = models.CharField(max_length=100, blank=True, help_text='Default name assigned to instances of this object. Should read like natural language.')
    description = models.TextField(blank=True)
    implements = models.ManyToManyField('Interface', limit_choices_to={'is_built_in': False}, blank=True, related_name='implemented_by', help_text='Interfaces implemented by this type.')
    visible = models.BooleanField(default=True)
    has_state = models.BooleanField(default=False)
    code = models.TextField(blank=True)
        
    class Meta:
        ordering = ['title']

    #--------------------------------------------------------------------------
    # Representation

    def __unicode__(self):
        # qs = self.template_parameters.all()
        return self.title or self.name # + (qs and u'<%s>' % ','.join([u'%s=%s' % (tp.name, tp.expression_text) for tp in qs]) or u'')

    #--------------------------------------------------------------------------
    # Queries
    
    binding_context = property(lambda self: self.template_bindings.get_context())
    context = property(lambda self: self.template_parameters.get_context())

    def _get_flat_expr(self):
        bc = self.binding_context
        return Expr.reduce([i.expr % bc for i in self.implements.all()])
    flat_expr = property(_get_flat_expr)

    def _get_expr(self):
        bc, c = self.binding_context, self.context
        return Expr.reduce([(i.expr % bc) % c for i in self.implements.all()])
    expr = property(_get_expr)
    
    # The final expression is used by objects when searching
    # for types that are compatible with a particular factory
    # parameter. We should have the final expression include
    # type template parameters so that resolve_to works properly.
    final_expr = property(lambda self: self.flat_expr)
    
    def show_all_expressions(self):
        s = lambda w: w.replace('<', '&lt;').replace('>', '&gt;')
        return '%s<br/>%s<br/>%s' % (s(`self.flat_expr`), s(`self.expr`), s(`self.final_expr`))
    show_all_expressions.short_description = 'Expressions'
    show_all_expressions.allow_tags = True
    
    def is_conflicted(self):
        '''
        Do two distinct methods of this type have the same name?
        Two methods are distinct if their signatures are different.
        Methods are included in types via interfaces. Some interfaces
        declare distinct methods with the same name. We must detect
        this problem early and notify the developer.
        '''
        return self.conflicting_methods().count() > 0
    is_conflicted.boolean = True

    def conflicting_methods(self):
        qs = Method.objects.filter(interface__implemented_by=self).distinct()
        counts = {}
        for method in qs:
            counts[method.name] = counts.get(method.name, 0) + 1
        names = [name for name, count in counts.items() if count > 1]
        return qs.filter(name__in=names).order_by('name')
    
    #--------------------------------------------------------------------------
    # Commands
                
    def generated_code(self):
        t = get_template('library/type/boilerplate.js')
        parsed = TypeCode(self)
        params = self.parameters.all()
        def f(attr):
            return filter(lambda p: getattr(p, attr), params)        
        c = Context({
            'type': self,
            'built_ins': f('is_built_in'),
            'references': f('is_ref'),
            'factories': f('is_factory'),
            'has_parameters': self.parameters.count() != 0,
            'methods': Method.objects.filter(interface__implemented_by=self).distinct(),
            'parsed': parsed,
        })
        return t.render(c)
        
    @classmethod
    def reset_code(cls):
        for type in cls.objects.all():
            type.code = type.generated_code()
            type.save()


###############################################################################
# PARAMETERS


class Parameter(models.Model):
    name = IdentifierField(unique=False)
    expression_text = ExprField('Expression')    
    # Cache to make searching for types more efficient
    _interfaces = models.ManyToManyField('Interface', editable=False)
    _is_built_in = models.BooleanField(editable=False)
    
    class Meta:
        ordering = ['name']
        abstract = True
    
    #--------------------------------------------------------------------------
    # Representation
    
    def __unicode__(self):
        return self.name
    
    #--------------------------------------------------------------------------
    # Queries

    is_built_in = property(lambda self: self._is_built_in)
    flat_expr = property(lambda self: Expr.parse(self.expression_text))
    interfaces = property(lambda self: Interface.objects.for_expr(self.expr))

    #--------------------------------------------------------------------------
    # Consistency (Cache maintenance)
    
    @staticmethod
    def pre_update_cache(sender, instance, **kwargs):
        instance._is_built_in = instance.expr.is_built_in

    @staticmethod
    def post_update_cache(sender, instance, **kwargs):
        instance._interfaces.clear()
        for interface in Interface.objects.for_expr(instance.expr):
            instance._interfaces.add(interface)
            

class TypeParameter(Parameter):
    of_type = models.ForeignKey(Type, related_name='parameters')
    is_factory = models.BooleanField(default=False)
    # Cache to make searching for types more efficient
    _is_ref = models.BooleanField(editable=False)
    
    #--------------------------------------------------------------------------
    # Queries
    
    is_ref = property(lambda self: not (self.is_built_in or self.is_factory))
    expr = property(lambda self: self.flat_expr % self.of_type.context)
    
    #--------------------------------------------------------------------------
    # Consistency (Cache maintenance)
    
    @staticmethod
    def pre_update_cache(sender, instance, **kwargs):
        instance._is_ref = not (instance.expr.is_built_in or instance.is_factory)

pre_save.connect(TypeParameter.pre_update_cache, sender=TypeParameter)
pre_save.connect(Parameter.pre_update_cache, sender=TypeParameter)
post_save.connect(Parameter.post_update_cache, sender=TypeParameter)


class MethodParameter(Parameter):
    of_method = models.ForeignKey(Method, related_name='parameters')    
    expr = property(lambda self: self.flat_expr % self.of_method.interface.context)
    
pre_save.connect(Parameter.pre_update_cache, sender=MethodParameter)
post_save.connect(Parameter.post_update_cache, sender=MethodParameter)


###############################################################################
# INTERFACE EXPRESSIONS PARAMETERS


class TemplateParameter(models.Model):
    name = IdentifierField(unique=False)
    expression_text = ExprField('Expression', help_text='What is the weakest interface required?')

    objects = ParameterManager()

    class Meta:
        abstract=True
        ordering = ['name']

    #--------------------------------------------------------------------------
    # Queries
    
    expr = property(lambda self: Expr.parse(self.expression_text))
    

class InterfaceTemplateParameter(TemplateParameter):
    of_interface = models.ForeignKey(Interface, related_name='template_parameters')

    def __unicode__(self):
        return '%s.%s' % (self.of_interface.name, self.name)


class TypeTemplateParameter(TemplateParameter):
    of_type = models.ForeignKey(Type, related_name='template_parameters')

    def __unicode__(self):
        return '@%s.%s' % (self.of_type.name, self.name)


###############################################################################
# INTERFACE EXPRESSION BINDINGS


class TemplateParameterBinding(models.Model):
    expression_text = ExprField('Expression')
    
    objects = ParameterManager()

    class Meta:
        abstract=True

    #--------------------------------------------------------------------------
    # Representation
    
    def __unicode__(self):
        return unicode(self.parameter)

    #--------------------------------------------------------------------------
    # Queries
    
    expr = property(lambda self: Expr.parse(self.expression_text))

    
class InterfaceTemplateParameterBinding(TemplateParameterBinding):
    type = models.ForeignKey(Type, related_name='template_bindings')
    parameter = models.ForeignKey(InterfaceTemplateParameter)
