'''
Storing collections of types and their configuration data to create compeleted games.
'''


import re
from django.db import models
from django.db.models import Q
from django.db.models.signals import *
from gamesoup.library.models import *


class Game(models.Model):
    '''
    A collection of modules and configuration that defines a Disposition game.
    '''
    name = models.CharField(max_length=50)
    slug = models.SlugField()
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


class Object(models.Model):
    '''
    An instance of a type.
    '''
    game = models.ForeignKey(Game)
    type = models.ForeignKey(Type)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=4)
    height = models.IntegerField(default=2)
    per_player = models.BooleanField(default=False)
    # parameter_bindings (See Binding.instance field)
    
    # Cached values
    satisfied = models.BooleanField(blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.type)
        
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
            return param.interface.is_built_in or Type.objects.filter(module__in_game=self.game, implements=param.interface).count() > 0
        return all(map(satisfiable, self.type.parameters.all()))

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        # Update cached values
        instance.satisfied = instance.parameter_bindings.count() == instance.type.parameters.count()

    @staticmethod
    def post_delete(sender, instance, **kwargs):
        # Remove any bindings which this object is a part of
        # Do this for both directions.
        instance.parameter_bindings.all().delete()
        instance.bound_to.all().delete()

pre_save.connect(Object.pre_save, sender=Object)        
post_delete.connect(Object.post_delete, sender=Object)


class Binding(models.Model):
    '''
    A parameter setting on an object.
    '''
    instance = models.ForeignKey(Object, related_name='parameter_bindings')
    parameter = models.ForeignKey(Variable, related_name='bindings')

    # Only one of the following 2 fields will be set depending on the nature of parameter.
    object_argument = models.ForeignKey('Object', blank=True, null=True, related_name='bound_to')
    built_in_argument = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.get_argument())
        
    def get_argument(self):
        if self.parameter.interface.is_built_in:
            return self.built_in_argument
        else:
            return 'object-%d' % self.object_argument.id
