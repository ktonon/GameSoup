'''
Storing collections of types and their configuration data to create compeleted games.
'''


import re
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import *
from gamesoup.library.models import *


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

    def possible_settings_for(self, variable):
        return self.object_set.filter(type__implements=variable.interface)

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
    game = models.ForeignKey(Game)
    type = models.ForeignKey(Type, related_name='instances')
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=5)
    height = models.IntegerField(default=5)
    per_player = models.BooleanField(default=False)
    # parameter_bindings (See TypeParameterBinding.instance field)
    
    # Cached values
    satisfied = models.BooleanField(blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.name or self.type)
    
    class Meta:
        ordering = ('name',)
        
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
            if param.is_built_in:
                # Built-in parameters are always satisfiable.
                return True
            else:                
                # For non-built-in parameters, the type must satisfy all
                # of the required interfaces.
                qs = Type.objects.filter(instances__game=self.game)
                for interface in param.interfaces.all():
                    qs = qs.filter(implements=interface)
                return qs.count() > 0
        return all(map(satisfiable, self.type.parameters.all()))

    def parameters_short(self):
        return ', '.join([p.name for p in self.type.parameters.all()])

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

    def __unicode__(self):
        return unicode(self.get_argument())
        
    def get_argument(self):
        if self.parameter.interface.is_built_in:
            return self.built_in_argument
        else:
            return '%d' % self.object_argument.id

post_save.connect(Object.update_cache, sender=TypeParameterBinding)
post_delete.connect(Object.update_cache, sender=TypeParameterBinding)


###############################################################################
# TEMPLATING

class TypeTemplateParameterBinding(TemplateParameterBinding):
    object = models.ForeignKey(Object)
    parameter = models.ForeignKey(TypeTemplateParameter)
