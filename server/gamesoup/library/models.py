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
        resolve = lambda expr: type and ((expr % bc) % c) or expr
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

    ###############################################################################
    # Dynamic
    
    expr = property(lambda self: Expr.parse('%s<%s>' % (self.name, self.context)))
    context = property(lambda self: self.template_parameters.get_context())
    
    ###############################################################################
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
    description = models.TextField(blank=True)
    implements = models.ManyToManyField('Interface', limit_choices_to={'is_built_in': False}, blank=True, related_name='implemented_by', help_text='Interfaces implemented by this type.')
    visible = models.BooleanField(default=True)
    has_state = models.BooleanField(default=False)
    code = models.TextField(blank=True)
    
    ###############################################################################
    # Dynamic

    def _get_expr(self):
        bc, c = self.binding_context, self.context
        return Expr.reduce([(i.expr % bc) % c for i in self.implements.all()])
    expr = property(_get_expr)
    
    context = property(lambda self: self.template_parameters.get_context())
    binding_context = property(lambda self: self.template_bindings.get_context())
    
    ###############################################################################
    # Representation
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        qs = self.template_parameters.all()
        return self.name + (qs and u'<%s>' % ','.join([u'%s=%s' % (tp.name, tp.expression_text) for tp in qs]) or u'')

    ###############################################################################
    # Queries
    
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
    
    ###############################################################################
    # Commands
                
    def generated_code(self):
        t = get_template('library/type/boilerplate.js')
        parsed = TypeCode(self)
        c = Context({
            'type': self,
            'built_ins': self.parameters.filter(is_built_in=True),
            'references': self.parameters.filter(is_built_in=False, is_factory=False),
            'factories': self.parameters.filter(is_built_in=False, is_factory=True),
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
    is_built_in = models.BooleanField(editable=False)
    
    class Meta:
        ordering = ['name']
        abstract = True
    
    def __unicode__(self):
        return self.name
    
    def get_expr(self):
        return Expr.parse(self.expression_text)
    expr = property(get_expr)
    
    @staticmethod
    def pre_save(sender, instance, **kwargs):
        expr = instance.expr
        instance.is_built_in = False
        if len(expr) == 1:
            try:
                instance.is_built_in = Interface.objects.get(name=expr.ids[0]).is_built_in
            except Interface.DoesNotExist:
                # It's ok, not a built in,
                # probably a variable
                pass

    @staticmethod
    def post_save(sender, instance, **kwargs):
        instance.interfaces.clear()
        for interface in Interface.objects.for_expr(instance.expr):
            instance.interfaces.add(interface)


class TypeParameter(Parameter):
    of_type = models.ForeignKey(Type, related_name='parameters')
    is_factory = models.BooleanField(default=False)
    interfaces = models.ManyToManyField(Interface, related_name='used_in_type_parameter', editable=False)
    
    def get_expr(self):
        expr = super(TypeParameter, self).get_expr()
        return expr % self.of_type.context
    expr = property(get_expr)
pre_save.connect(Parameter.pre_save, sender=TypeParameter)
post_save.connect(Parameter.post_save, sender=TypeParameter)


class MethodParameter(Parameter):
    of_method = models.ForeignKey(Method, related_name='parameters')
    interfaces = models.ManyToManyField(Interface, related_name='used_in_method_parameter', editable=False)
pre_save.connect(Parameter.pre_save, sender=MethodParameter)
post_save.connect(Parameter.post_save, sender=MethodParameter)


###############################################################################
# TEMPLATING


class TemplateParameter(models.Model):
    name = IdentifierField(unique=False)
    expression_text = ExprField('Expression', help_text='What is the weakest interface required?')

    objects = ParameterManager()

    class Meta:
        abstract=True
        ordering = ['name']

    def __unicode__(self):
        return '.'.join([self.of.name, self.name])

    def get_expr(self):
        return Expr.parse(self.expression_text)
    expr = property(get_expr)
    

class TemplateParameterBinding(models.Model):
    expression_text = ExprField('Expression')
    
    objects = ParameterManager()

    class Meta:
        abstract=True
            
    def __unicode__(self):
        return unicode(self.parameter)

    def get_expr(self):
        return Expr.parse(self.expression_text)
    expr = property(get_expr)


# PARAMETERS


class InterfaceTemplateParameter(TemplateParameter):
    of_interface = models.ForeignKey(Interface, related_name='template_parameters')
    of = property(lambda self: self.of_interface)


class TypeTemplateParameter(TemplateParameter):
    of_type = models.ForeignKey(Type, related_name='template_parameters')
    of = property(lambda self: self.of_type)

    def __unicode__(self):
        return '@' + super(TypeTemplateParameter, self).__unicode__()


# BINDINGS

    
class InterfaceTemplateParameterBinding(TemplateParameterBinding):
    type = models.ForeignKey(Type, related_name='template_bindings')
    parameter = models.ForeignKey(InterfaceTemplateParameter)
