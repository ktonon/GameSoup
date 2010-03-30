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
from gamesoup.library.parsers import *
from gamesoup.library.code import TypeCode


class Method(models.Model):
    '''
    Method signature.
    '''
    interface = models.ForeignKey('Interface', related_name='methods')
    name = models.CharField(max_length=200, blank=True, editable=False)
    description = models.TextField(blank=True)
    parameters = models.ManyToManyField('Variable', related_name='parameter_of_method', blank=True, editable=False)
    returned = models.ForeignKey('Variable', related_name='returned_from_method', blank=True, editable=False)
    signature = SignatureField(parse_method_signature, unique=True)
    # parameters -- See MethodParameter#of_method

    objects = SignatureManager()

    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return self.signature
    
    @staticmethod
    def pre_save(sender, instance, **kwargs):
        d = parse_method_signature(instance.signature)
        instance.name = d['name']
        instance.returned = d['returned']

    @staticmethod
    def post_save(sender, instance, **kwargs):
        d = parse_method_signature(instance.signature)
        instance.parameters.add(*d['parameters'])

pre_save.connect(Method.pre_save, sender=Method)
post_save.connect(Method.post_save, sender=Method)


class Interface(models.Model):
    '''
    A set of public methods available on instances of an object.
    Interfaces can be abstracted using template parameters.
    '''
    name = IdentifierField(help_text='A unique name. Should be specified using MixedCase with no spaces.')
    description = models.TextField(blank=True, help_text='This will serve as a human-readable, searchable account of this interface. Make this very detailed, because this will be the primary description of this interface for game designers.')
    is_built_in = models.BooleanField(default=False, help_text="Built-in interfaces are provided by the underlying language (JavaScript) or library (Prototype) and do not require a Type to be implemented.")
    
    objects = InterfaceManager()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        qs = self.template_parameters.all()
        return self.name + (qs and u'<%s>' % ','.join([u'%s=%s' % (tp.name, tp.weakest) for tp in qs]) or u'')

    def implemented_by_short(self):
        return ', '.join([type.name for type in self.implemented_by.all()])
    implemented_by_short.short_description = 'Implemented by'

    def doc_link(self):
        return '<a href="%s">%s</a>' % (
            reverse('library:interface_documentation', args=[self.id]),
            '<br/>'.join([m.name for m in self.methods.all()])
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
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

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
    
    def generated_code(self):
        t = get_template('library/type/boilerplate.js')
        parsed = TypeCode(self)
        c = Context({
            'type': self,
            'built_ins': self.parameters.filter(is_built_in=True),
            'references': self.parameters.filter(is_built_in=False),
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
    expression = InterfaceExpressionField()
    is_built_in = models.BooleanField(editable=False)
    interfaces = models.ManyToManyField(Interface, related_name='used_in_parameter', editable=False)
    
    class Meta:
        ordering = ['name']
        abstract = True
    
    def __unicode__(self):
        return self.name

    def get_interface(self):
        if self.interfaces.count() > 1:
            raise Exception('There are more than one interface for the parameter %s' % self.name)
        return self.interfaces.all()[0]
    interface = property(get_interface)
    
    @staticmethod
    def pre_save(sender, instance, **kwargs):
        exp = InterfaceExpression(instance.expression)
        instance.is_built_in = exp.is_built_in
        instance.interfaces.clear()
        for interface in exp.interfaces:
            instance.interfaces.add(interface)


class TypeParameter(Parameter):
    of_type = models.ForeignKey(Type, related_name='parameters')
    of = property(lambda self: self.of_type)
pre_save.connect(Parameter.pre_save, sender=TypeParameter)


# class MethodParameter(Parameter):
#     of_method = models.ForeignKey(Method)#, related_name='parameters')
#     of = property(lambda self: self.of_method)
# pre_save.connect(Parameter.pre_save, sender=MethodParameter)

    
class Variable(models.Model):
    '''
    A variable declaration.
    '''
    name = models.CharField(max_length=100, blank=True, editable=False)
    interface_name = models.CharField(max_length=100, blank=True, editable=False)
    interface = models.ForeignKey('Interface', blank=True, editable=False, null=True)
    interface_expression = InterfaceExpressionField(editable=False)
    signature = SignatureField(parse_variable_signature, unique=True)

    class Meta:
        ordering = ['name']

    objects = SignatureManager()
    
    def __unicode__(self):
        return self.signature
        
    @staticmethod
    def pre_save(sender, instance, **kwargs):
        d = parse_variable_signature(instance.signature)
        instance.name = d['name']
        instance.interface = d['interface']
        instance.interface_name = d['interface_name']
        instance.interface_expression = instance.interface_name + (d['template_arguments'] or '')

pre_save.connect(Variable.pre_save, sender=Variable)


###############################################################################
# TEMPLATING


class TemplateParameter(models.Model):
    name = IdentifierField(unique=False)
    weakest = InterfaceExpressionField(help_text='What is the weakest interface required?')

    class Meta:
        abstract=True
        ordering = ['name']

    def __unicode__(self):
        return '%s::%s' % (self.of.name, self.name)


class TemplateParameterBinding(models.Model):
    bound_to = InterfaceExpressionField()
    
    class Meta:
        abstract=True
            
    def __unicode__(self):
        return self.bound_to

# PARAMETERS

class InterfaceTemplateParameter(TemplateParameter):
    of_interface = models.ForeignKey(Interface, related_name='template_parameters')
    of = property(lambda self: self.of_interface)

class TypeTemplateParameter(TemplateParameter):
    of_type = models.ForeignKey(Type, related_name='template_parameters')
    of = property(lambda self: self.of_type)

# BINDINGS
    
class InterfaceTemplateParameterBinding(TemplateParameterBinding):
    type = models.ForeignKey(Type)
    parameter = models.ForeignKey(InterfaceTemplateParameter)
