'''
Stores the components from which games are made. The most important of these are types.
'''


import re
from django.db import models
from django.db.models import Q
from django.db.models.signals import *
from alphacabbage.django.choices import *
from gamesoup.library.errors import *
from gamesoup.library.fields import *
from gamesoup.library.managers import *
from gamesoup.library.parsers import *


class Interface(models.Model):
    '''
    A set of public methods available on instances of an object.
    '''
    name = IdentifierField()
    description = models.TextField(blank=True)
    methods = models.ManyToManyField('Method', related_name='used_in_interface', blank=True, editable=False)
    signature = SignatureField(parse_interface_signature, verbose_name='Methods', multiline=True, blank=True)
    is_built_in = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @staticmethod
    def post_save(sender, instance, **kwargs):
        # Remove old methods
        for method in instance.methods.all():
            instance.methods.remove(method)
        # Add new methods
        d = parse_interface_signature(instance.signature)
        instance.methods.add(*d['methods'])

post_save.connect(Interface.post_save, sender=Interface)


class Type(models.Model):
    '''
    An instantiable type.
    Types can implement multiple interfaces.
    '''
    name = IdentifierField()
    description = models.TextField(blank=True)
    implements = models.ManyToManyField('Interface', limit_choices_to={'is_built_in': False}, blank=True, related_name='implemented_by', help_text='Interfaces implemented by this type.')
    parameters = models.ManyToManyField('Variable', related_name='parameter_of_type', blank=True, editable=False)
    signature = SignatureField(parse_type_signature, verbose_name='Parameters', multiline=True, blank=True)
    visible = models.BooleanField(default=True)
    has_state = models.BooleanField(default=False)
    code = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

    @staticmethod
    def post_save(sender, instance, **kwargs):
        # Parse signature and set parameters
        d = parse_type_signature(instance.signature)
        instance.parameters.add(*d['parameters'])

post_save.connect(Type.post_save, sender=Type)


class Method(models.Model):
    '''
    Method signature.
    '''
    name = models.CharField(max_length=200, blank=True, editable=False)
    parameters = models.ManyToManyField('Variable', related_name='parameter_of_method', blank=True, editable=False)
    returned = models.ForeignKey('Variable', related_name='returned_from_method', blank=True, editable=False)
    signature = SignatureField(parse_method_signature, unique=True)

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


class Variable(models.Model):
    '''
    A variable declaration.
    '''
    name = models.CharField(max_length=100, blank=True, editable=False)
    interface = models.ForeignKey('Interface', blank=True, editable=False)
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

pre_save.connect(Variable.pre_save, sender=Variable)
