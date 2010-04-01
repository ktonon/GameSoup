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


class Method(models.Model):
    '''
    Method signature.
    '''
    interface = models.ForeignKey('Interface', related_name='methods')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    return_expression = InterfaceExpressionField('Return', default='Nothing')
    # parameters -- See MethodParameter#of_method

    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return self.signature
    
    def get_signature(self, as_implemented_by_type=None):
        from gamesoup.library.expressions.semantics import InterfaceExpression
        context = self.interface.template_context
        if as_implemented_by_type:
            as_implemented_by_type.update_interface_template_context(self.interface, context)
            c = as_implemented_by_type.template_context
            context = dict([
                (k, InterfaceExpression.parse(expr.resolve(c)))
                for k, expr in context.items()
                ])
        print context
        params = []
        for method_param in self.parameters.all():
            expr = InterfaceExpression.parse(method_param.expression)
            expr_text = expr.resolve(context)
            params.append('%s : %s' % (method_param.name, expr_text))
        w = u'%s(%s)' % (self.name, ' ; '.join(params))
        if self.return_expression != 'Nothing':
            w += ' : %s' % InterfaceExpression.parse(self.return_expression).resolve(context)
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

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        qs = self.template_parameters.all()
        return self.name + (qs and u'<%s>' % ','.join([u'%s=%s' % (tp.name, tp.weakest) for tp in qs]) or u'')

    def is_nothing(self):
        return self == self.__class__.objects.nothing()

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

    def _get_template_context(self):
        from gamesoup.library.expressions.semantics import InterfaceExpression
        context = {}
        for template_param in self.template_parameters.all():
            context[template_param.name] = InterfaceExpression.parse(template_param.weakest)
        return context
    template_context = property(_get_template_context)

    
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
    
    def _get_template_context(self):
        from gamesoup.library.expressions.semantics import InterfaceExpression
        context = {}
        for template_param in self.template_parameters.all():
            context[template_param.name] = InterfaceExpression.parse(template_param.weakest)
        return context
    template_context = property(_get_template_context)
    
    def update_interface_template_context(self, interface, context):
        '''
        Update an interfaces template context with template parameter bindings from this type.
        '''
        from django.core.exceptions import MultipleObjectsReturned
        from gamesoup.library.expressions.semantics import InterfaceExpression
        for variable_id, expr in context.items():
            try:
                binding = self.interfacetemplateparameterbinding_set.get(parameter__name=variable_id, parameter__of_interface=interface)
                context[variable_id] = InterfaceExpression.parse(binding.bound_to)
            except InterfaceTemplateParameterBinding.DoesNotExist:
                pass
            except MultipleObjectsReturned, e:
                print self.name
                raise e
    
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
    expression = InterfaceExpressionField()
    is_built_in = models.BooleanField(editable=False)
    
    class Meta:
        ordering = ['name']
        abstract = True
    
    def __unicode__(self):
        return self.name

    def get_interface(self):
        if self.interfaces.count() > 1:
            from traceback import print_stack
            print_stack()
            raise Exception('There are more than one interfaces for the parameter %s' % self.name)
        return self.interfaces.all()[0]
    interface = property(get_interface)
    
    @staticmethod
    def pre_save(sender, instance, **kwargs):
        from gamesoup.library.expressions.semantics import InterfaceExpression
        expr = InterfaceExpression.parse(instance.expression)
        instance.is_built_in = expr.is_atomic and not expr[0].is_variable and expr[0].interface.is_built_in

    @staticmethod
    def post_save(sender, instance, **kwargs):
        from gamesoup.library.expressions.semantics import InterfaceExpression
        expr = InterfaceExpression.parse(instance.expression)
        instance.interfaces.clear()
        for interface in expr.interfaces:
            instance.interfaces.add(interface)


class TypeParameter(Parameter):
    of_type = models.ForeignKey(Type, related_name='parameters')
    is_factory = models.BooleanField(default=False)
    interfaces = models.ManyToManyField(Interface, related_name='used_in_type_parameter', editable=False)
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
