'''
Storing collections of types and their configuration data to create compeleted games.
'''


import re
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import *
from gamesoup.library.models import *
from gamesoup.expressions.syntax import Expr


class Game(models.Model):
    '''
    A collection of modules and configuration that defines a Disposition game.
    '''
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

    def is_satisfied(self):
        return self.object_set.filter(satisfied=False).count() == 0
    is_satisfied.boolean = True

    def get_assembler_link(self):
        return '<a href="%s" title="Assemble this game">Objects: %d</a>' % (reverse('games:assemble_game', args=[self.id]), self.object_set.count())
    get_assembler_link.short_description = 'Assembler'
    get_assembler_link.allow_tags = True

    def code_url(self):
        return reverse('games:game_code', args=[self.id])

    def code_link(self):
        return '<a href="%s" title="See the source code for this game">Code</a>' % self.code_url()
    code_link.short_description = 'Code'
    code_link.allow_tags = True

    def is_empty(self):
        return self.object_set.count() == 0
    
    def palette_query(self):
        return 'instances__game=%d' % self.id


class Object(models.Model):
    '''
    An instance of a type.
    '''
    name = models.CharField(max_length=50, blank=True)
    game = models.ForeignKey(Game, editable=False)
    type = models.ForeignKey(Type, related_name='instances', editable=False)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=5)
    height = models.IntegerField(default=5)
    per_player = models.BooleanField(default=False)
    # parameter_bindings (See TypeParameterBinding.instance field)
    
    # Cached values
    satisfied = models.BooleanField(blank=True)
    
    ###############################################################################
    # Dynamic

    binding_context = property(lambda self: self.template_bindings.get_context())
    context = property(lambda self: self.template_parameters.get_context())
    final_context = property(lambda self: self.final_bindings.get_context())

    flat_expr = property(lambda self: self.type.flat_expr % self.binding_context)
    expr = property(lambda self: self.flat_expr % self.context)
    final_expr = property(lambda self: self.flat_expr % self.final_context)
    
    ###############################################################################
    # Representation
    
    def __unicode__(self):
        return u'%s' % (self.name or self.type)
    
    class Meta:
        ordering = ('name',)

    def parameters_short(self):
        return ', '.join([p.name for p in self.type.parameters.all()])
    
    ###############################################################################
    # Queries
    
    def is_satisfied(self):
        '''
        Have all the type parameters been bound?
        '''
        x = self.parameter_bindings.count() == self.type.parameters.count()
        # Cache if needed
        if self.satisfied != x:
            self.save()
        return x
    
    def is_satisfiable(self):
        '''
        Given the current types in the game, is it possible to satisfy this object?
        '''
        def satisfiable(param):
            # Is there a type in the game for the required interface?
            if param.is_built_in or param.is_factory:
                # Built-in parameters are always satisfiable.
                return True
            else:                
                # For non-built-in parameters, the type must satisfy all
                # of the required interfaces.
                qs = Type.objects.filter(instances__game=self.game)
                expr = Expr.parse(param.expression_text)
                for interface in Interface.objects.for_expr(expr):
                    qs = qs.filter(implements=interface)
                return qs.count() > 0
        return all(map(satisfiable, self.type.parameters.all()))

    def bindable_to(self, other, param):
        '''
        Is self bindable to the given param of the other object?
        '''
        # The parameter of the other object is an instance
        # of TypeParameter with the following fields:
        #   name
        #   expression_text
        #   is_built_in
        #   of_type
        #   is_factory
        #   interfaces
        #
        a = self.final_expr
        b = param.expr % other.binding_context % other.final_context
        print 'Attempting to bind %s to %s' % (a, b)
        r = a.resolvent_for(b)
        ar = a % r
        print '%s %% %s resolves to %s' % (a, r, ar)
        print 'and %s.super(%s) is %s' % (ar, b, ar.super(b))
        # TODO: if self gets bound to param, make sure
        # to create an ObjectTemplateParameterBinding!
        # Not here thought, is the view that does the binding!
        return ar.super(b)

    def used_by(self):
        qs = Object.objects.filter(parameter_bindings__object_argument=self)
        return qs
    
    def expressions_required_by_users(self):
        '''
        A set of interface expressions which are required of this object by
        other objects which bind it as a parameter.
        '''
        return []
        
    ###############################################################################
    # Commands

    @staticmethod
    def post_delete(sender, instance, **kwargs):
        # Remove any bindings which this object is a part of
        # Do this for both directions.
        instance.parameter_bindings.all().delete()
        instance.bound_to.all().delete()
    
    @staticmethod
    def post_save(sender, instance, **kwargs):
        if instance.name == '':
            instance.name = instance.type.name
            instance.save() # Since name is set, this should avoid infinite recursion

    @staticmethod
    def make_template_parameters_and_bindings(sender, instance, **kwargs):
        # Make the default ObjectTemplateParamters and
        # TypeTemplateParameterBindings
        obj = instance
        for tp in obj.type.template_parameters.all():
            key = '%d.%s' % (obj.id, tp.name)
            print key
            try:
                op = obj.template_parameters.get(name=tp.name)
            except ObjectTemplateParameter.DoesNotExist:
                op = obj.template_parameters.create(name=tp.name, expression_text=tp.expression_text)
                tb = obj.template_bindings.create(parameter=tp, expression_text=key)
            except ObjectTemplateParameter.MultipleObjectsReturned:
                pass
        print obj.template_parameters.all()
        print obj.template_bindings.all()
        
    @staticmethod
    def update_cache(sender, instance, **kwargs):
        if sender.__name__ == 'TypeParameterBinding':
            obj = instance.instance
        else:
            obj = instance
        sat = obj.parameter_bindings.count() == obj.type.parameters.count()
        if obj.satisfied != sat:
            obj.satisfied = sat
            if sender != obj.__class__:
                obj.save()

pre_save.connect(Object.update_cache, sender=Object)
post_save.connect(Object.post_save, sender=Object)
post_save.connect(Object.make_template_parameters_and_bindings, sender=Object)
post_delete.connect(Object.post_delete, sender=Object)


class TypeParameterBinding(models.Model):
    '''
    A parameter setting on an object.
    '''
    instance = models.ForeignKey(Object, related_name='parameter_bindings')
    parameter = models.ForeignKey(TypeParameter, related_name='bindings')

    # Only one of the following 2 fields will be set depending on the nature of parameter.
    object_argument = models.ForeignKey('Object', blank=True, null=True, related_name='bound_to')
    built_in_argument = models.TextField(blank=True)
    type_argument = models.ForeignKey(Type, blank=True, null=True, related_name='bound_to')

    def __unicode__(self):
        return unicode(self.get_argument())
    
    class Meta:
        ordering = ('parameter',)

    def get_kind(self):
        if self.parameter.is_built_in:
            return 'built-in'
        else:
            if self.parameter.is_factory:
                return 'factory'
            else:
                return 'reference'

    def get_argument(self):
        if self.parameter.is_built_in:
            return self.built_in_argument
        else:
            if self.parameter.is_factory:
                return '%d' % self.type_argument.id
            else:
                return '%d' % self.object_argument.id

    def get_argument_link(self):
        if self.parameter.is_built_in:
            return self.built_in_argument
        else:
            if self.parameter.is_factory:
                return '<a href="%s">%s</a>' % (reverse('admin:library_type_change', args=[self.type_argument.id]), self.type_argument)
            else:
                return '<a href="%s">%s</a>' % (reverse('admin:games_object_change', args=[self.object_argument.id]), self.object_argument)


post_save.connect(Object.update_cache, sender=TypeParameterBinding)
post_delete.connect(Object.update_cache, sender=TypeParameterBinding)


###############################################################################
# TEMPLATING

class ObjectTemplateParameter(TemplateParameter):
    of_object = models.ForeignKey(Object, related_name='template_parameters')
    of = property(lambda self: self.of_object)
    
    def __unicode__(self):
        return u'%d.%s' % (self.of_object.id, self.name)


class TypeTemplateParameterBinding(TemplateParameterBinding):
    object = models.ForeignKey(Object, related_name='template_bindings')
    parameter = models.ForeignKey(TypeTemplateParameter)

    def __unicode__(self):
        return unicode(self.parameter)


class ObjectTemplateParameterBinding(TemplateParameterBinding):
    object = models.ForeignKey(Object, related_name='final_bindings')
    parameter = models.ForeignKey(ObjectTemplateParameter)

    def __unicode__(self):
        return unicode(self.parameter)
