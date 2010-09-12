'''
Storing collections of types and their configuration data to create compeleted games.
'''

import datetime, re
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import *
from gamesoup.library.models import *
from gamesoup.expressions.syntax import Expr
from gamesoup.games.managers import *


###############################################################################
# PARAMETERS AND OBJECT CONNECTIONS


class ObjectParameter(models.Model):
    of_object = models.ForeignKey('Object', related_name='parameters')
    type_parameter = models.ForeignKey(TypeParameter, related_name='object_parameters')

    #--------------------------------------------------------------------------
    # Representation
    
    def __unicode__(self):
        return unicode(self.type_parameter)

    kind = property(lambda self: (self.is_built_in and 'built-in') or (self.is_factory and 'factory') or 'reference')
    css_classes = property(lambda self: self.binding and ('bound %s' % self.kind) or 'unbound')
    
    #--------------------------------------------------------------------------
    # Queries
    
    name = property(lambda self: self.type_parameter.name)
    is_built_in = property(lambda self: self.type_parameter.is_built_in)
    is_factory = property(lambda self: self.type_parameter.is_factory)    
    is_ref = property(lambda self: self.type_parameter.is_ref)
    game = property(lambda self: self.of_object.game)
    
    def _binding_or_none(self):
        try:
            return self._binding
        except ObjectParameterBinding.DoesNotExist:
            return None
    binding = property(_binding_or_none)
    
    # Expressions representing this object
    #   flat_expr       - an expression involving object variables
    #   context         - an expression with default values applied
    #   final_expr      - an expression with bound expressions applied
    #
    flat_expr = property(lambda self: self.type_parameter.flat_expr % self.of_object.binding_context)
    expr = property(lambda self: self.flat_expr % self.of_object.context)
    final_expr = property(lambda self: self.flat_expr % self.of_object.final_context % self.of_object.context)

    # Use the final expression to get a queryset of Interfaces
    # that any bound object or type must support
    interfaces = property(lambda self: Interface.objects.for_expr(self.final_expr))

    def resolvent_for(self, component):
        '''
        Can this parameter be bound to the given component?
        If the parameter can be bound, returns the resolvent
        which makes this possible, otherwise returns None.
        '''
        a = component.final_expr
        b = self.final_expr
        r = a.resolvent_for(b)

        # Does r work for obj?
        if not (a % r).is_super(b): return None
        # It does!
        # However, will the game as a whole be happy about it?
        if not self.game.can_apply_resolvent(r): return None
        # Ok, we are good!
        return r
        
    def _candidate_objects(self):
        '''
        Objects in the game that can satisfy this reference parameter.
        '''
        assert self.is_ref
        qs = Object.objects.filter(game=self.of_object.game)
        for interface in self.interfaces:
            qs = qs.filter(type__implements=interface)
        if self.of_object.name == 'Word on board?' and self.name == 'board':
            print qs
        return [obj for obj in qs if self.resolvent_for(obj) is not None]
    candidate_objects = property(_candidate_objects)

    def _candidate_types(self):
        '''
        Types in the library that can satisfy this parameter.
        This can be done for both references and factory parameters.
        '''
        qs = Type.objects.all()
        for interface in self.interfaces:
            qs = qs.filter(implements=interface)
        if self.is_factory:
            qs = qs.filter(parameters__isnull=True).distinct()
        def has_resolvent(t):
            resolvent = self.resolvent_for(t)
            return resolvent is not None
        return filter(has_resolvent, qs)
        # return [t for t in qs if self.resolvent_for(t) is not None]
    candidate_types = property(_candidate_types)

    # For parameters which refer to other objects, are there any objects
    # in the game that can satisfy them?
    # Built-ins and factories are always considered satisfiable.
    is_satisfiable = property(lambda self: self.is_built_in or self.is_factory or len(self.candidate_objects) > 0)
    
    #--------------------------------------------------------------------------
    # Commands
    
    def bind(self, value):
        '''
        Bind value.
        '''
        # Remove the old binding.
        self.binding and self.binding.delete()
                
        # Add the new binding
        binding = ObjectParameterBinding(instance=self.of_object, parameter=self)
        if self.is_built_in:
            binding.built_in_argument = value
        elif self.is_factory:
            type = Type.objects.get(pk=getattr(value, 'id', value))
            r = self.resolvent_for(type)
            assert r is not None
            binding.type_argument = type
            self.game.apply_resolvent(r)
        else:
            obj = Object.objects.get(pk=getattr(value, 'id', value))
            r = self.resolvent_for(obj)
            assert r is not None
            binding.object_argument = obj
            self.game.apply_resolvent(r)
        binding.save()
        return binding.argument

    
class ObjectParameterBinding(models.Model):
    '''
    A parameter setting on an object.
    '''
    instance = models.ForeignKey('Object', related_name='bindings')
    parameter = models.OneToOneField('ObjectParameter', related_name='_binding')
    # Only one of the following 3 fields will be set depending on the nature of parameter.
    built_in_argument = models.TextField(blank=True)
    type_argument = models.ForeignKey(Type, blank=True, null=True, related_name='bound_to')
    object_argument = models.ForeignKey('Object', blank=True, null=True, related_name='bound_to')

    class Meta:
        ordering = ('parameter',)

    #--------------------------------------------------------------------------
    # Representation
    
    def __unicode__(self):
        return unicode(self.argument)

    def get_argument_link(self):
        if self.parameter.is_built_in:
            return self.built_in_argument
        else:
            if self.parameter.is_factory:
                return '<a href="%s">%s</a>' % (reverse('admin:library_type_change', args=[self.type_argument.id]), self.type_argument)
            else:
                return '<a href="%s">%s</a>' % (reverse('admin:games_object_change', args=[self.object_argument.id]), self.object_argument)

    #--------------------------------------------------------------------------
    # Queries

    argument = property(lambda self: 
        (self.parameter.is_built_in and self.built_in_argument) or
        (self.parameter.is_factory and self.type_argument) or
        self.object_argument)

    #--------------------------------------------------------------------------
    # Consistency
    
    @staticmethod
    def post_delete(sender, instance, **kwargs):
        # When a binding is deleted
        pass

post_delete.connect(ObjectParameterBinding.post_delete, sender=ObjectParameterBinding)


###############################################################################
# INTERFACE_EXPRESSIONS


class TypeTemplateParameterBinding(TemplateParameterBinding):
    object = models.ForeignKey('Object', related_name='template_bindings')
    parameter = models.ForeignKey(TypeTemplateParameter)

    def __unicode__(self):
        return unicode(self.parameter)


class ObjectTemplateParameter(TemplateParameter):
    of_object = models.ForeignKey('Object', related_name='template_parameters')
    
    def __unicode__(self):
        return u'%d.%s' % (self.of_object.id, self.name)

    #--------------------------------------------------------------------------
    # Queries
    
    final_expr = property(lambda self: self.binding and self.binding.expr or self.expr)

    def _binding_or_none(self):
        try:
            return self._binding
        except ObjectTemplateParameterBinding.DoesNotExist:
            return None
    binding = property(_binding_or_none)
    
    #--------------------------------------------------------------------------
    # Commands
    
    def can_update_with(self, expr):
        '''
        Can this template parameter be updated with the given expression?
        '''
        e = self.final_expr
        if e.is_var:
            return True
        else:
            return expr.is_super(e)

    def update(self, expr):
        '''
        Update the binding for this template parameter with expr.
        
        If no binding exists, a new one is created.
        '''
        assert self.can_update_with(expr)
        if self.binding:
            self.binding.expression_text = `expr`
            self.binding.save()
        else:
            ObjectTemplateParameterBinding.objects.create(
                object=self.of_object,
                parameter=self,
                expression_text=`expr`
                )


class ObjectTemplateParameterBinding(TemplateParameterBinding):
    object = models.ForeignKey('Object', related_name='final_bindings')
    parameter = models.OneToOneField('ObjectTemplateParameter', related_name='_binding')

    def __unicode__(self):
        return unicode(self.parameter)


###############################################################################
# GAMES AND OBJECTS


class Game(models.Model):
    '''
    A collection of modules and configuration that defines a Disposition game.
    '''
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        ordering = ['name']
    
    #--------------------------------------------------------------------------
    # Representation
    
    def __unicode__(self):
        return self.name

    #--------------------------------------------------------------------------
    # Links
    
    def get_assembler_link(self):
        return '<a href="%s" title="Assemble this game">Objects: %d</a>' % (reverse('games:assemble_game', args=[self.id]), self.object_set.count())
    get_assembler_link.short_description = 'Assembler'
    get_assembler_link.allow_tags = True

    def code_link(self):
        return '<a href="%s" title="See the source code for this game">Code</a>' % reverse('games:game_code', args=[self.id])
    code_link.short_description = 'Code'
    code_link.allow_tags = True

    #--------------------------------------------------------------------------
    # Queries

    # Are all the objects in the game satisfied?
    is_satisfied = property(lambda self: all([obj.is_satisfied for obj in self.object_set.all()]))

    def can_apply_resolvent(self, r):
        '''
        Can the resolvent r be applied to this game?
        That is, if we apply r to this game, will it still be in
        a consistent state?
        '''            
        # To answer this question, we need to apply r to every object
        # in the game and see if any existing connections break.
        # TODO: implement me!
        return True

    #--------------------------------------------------------------------------
    # Commands
    
    def apply_resolvent(self, r):
        '''
        Apply the resolvent r to this game.
        
        Assumes that Game#can_apply_resolvent has already been called
        to see if r is even legal.
        '''
        for obj in self.object_set.all():
            obj.apply_resolvent(r)
    
    def mark_as_updated(self):
        '''
        Set the update_at field to indicate that this game was changed recently.
        '''
        self.updated_at = datetime.datetime.now()
        self.save()
        

class Object(models.Model):
    '''
    An instance of a type.
    '''
    name = models.CharField(max_length=50, blank=True)
    game = models.ForeignKey('Game', editable=False)
    type = models.ForeignKey(Type, related_name='instances', editable=False)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=5)
    height = models.IntegerField(default=5)
    per_player = models.BooleanField(default=False)

    objects = GameObjectManager()
    
    class Meta:
        ordering = ('name',)

    #--------------------------------------------------------------------------
    # Representation
        
    def __unicode__(self):
        return u'%s' % (self.name or self.type)
    
    #--------------------------------------------------------------------------
    # Queries

    # Contexts for resolving variables in expressions
    #   binding_context - replaces type variables with object variables
    #   context         - replaces object variables with default values
    #   final_context   - replaces object variables with bound expressions
    #
    binding_context = property(lambda self: self.template_bindings.get_context())
    context = property(lambda self: self.template_parameters.get_context())
    final_context = property(lambda self: self.final_bindings.get_context())

    # Expressions representing this object
    #   flat_expr       - an expression involving object variables
    #   expr            - an expression with default values applied
    #   final_expr      - an expression with bound expressions applied
    #
    flat_expr = property(lambda self: self.type.flat_expr % self.binding_context)
    expr = property(lambda self: self.flat_expr % self.context)
    final_expr = property(lambda self: self.flat_expr % self.final_context)

    # Are all the type parameters bound?
    is_satisfied = property(lambda self: self.parameters.count() == self.bindings.count())

    # Can all the object reference parameters be bound?
    is_satisfiable = property(lambda self: all([p.is_satisfiable for p in self.parameters.all()]))

    def get_parameter(self, name):
        return self.parameters.get(type_parameter__name=name)
    
    #--------------------------------------------------------------------------
    # Commands

    def bind_parameter(self, name, value):
        self.get_parameter(name).bind(value)

    def apply_resolvent(self, r):
        '''
        Apply the resolvent r to this object.
        '''
        # Apply r to each object in the game.
        # TODO: implement me!
        for key, expr in r.items():
            qualifier, name = key.split('.')
            if str(self.id) != qualifier: 
                # Only apply resolvents that target this object.
                continue
            try:
                param = self.template_parameters.get(name=name)
                param.update(expr)
            except ObjectTemplateParameter.DoesNotExist:
                # Ok, not applicable to this object.
                pass

    #--------------------------------------------------------------------------
    # Consistency

    @staticmethod
    def mark_game_as_updated(sender, instance, **kwargs):
        instance.game.mark_as_updated()

    @staticmethod
    def post_save(sender, instance, **kwargs):
        obj = instance

        # Make the default ObjectTemplateParamters and
        # TypeTemplateParameterBindings
        for tp in obj.type.template_parameters.all():
            try:
                obj.template_bindings.get(parameter=tp)
            except TypeTemplateParameterBinding.DoesNotExist:
                # Binding which replaces @Type.var with 1.var
                obj.template_bindings.create(parameter=tp, expression_text='%d.%s' % (obj.id, tp.name))
                # The parameter 1.var
                obj.template_parameters.create(name=tp.name, expression_text=tp.expression_text)

        # Make ObjectParameters
        for tp in obj.type.parameters.all():
            try:
                obj.parameters.get(type_parameter=tp)
            except ObjectParameter.DoesNotExist:
                obj.parameters.create(type_parameter=tp)
        
        # Give the object a default name
        if obj.name == '':
            obj.name = obj.type.title or obj.type.name
            obj.save() # Since name is set, this should avoid infinite recursion

    @staticmethod
    def post_delete(sender, instance, **kwargs):
        # Remove any bindings which this object is a part of
        # Do this for both directions.
        instance.bindings.all().delete()
        instance.bound_to.all().delete()

        # Remove object parameters
        instance.parameters.all().delete()

        # Remove template parameters and bindings
        instance.final_bindings.all().delete()
        instance.template_bindings.all().delete()
        instance.template_parameters.all().delete()
        
pre_save.connect(Object.mark_game_as_updated, sender=Object)
pre_delete.connect(Object.mark_game_as_updated, sender=Object)
post_save.connect(Object.post_save, sender=Object)
post_delete.connect(Object.post_delete, sender=Object)


# from alphacabbage.tracer import Tracer
# tracer = Tracer(ObjectParameter, ObjectTemplateParameter)
