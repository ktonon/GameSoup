'''
Custom fields for the build app.
'''


import re
from django.db import models
from django import forms
from gamesoup.library.errors import *


__all__ = (
    'SignatureField',
    'IdentifierField',
    )


class SignatureFormField(forms.CharField):

    def __init__(self, parser_function, *args, **kwargs):
        super(SignatureFormField, self).__init__(*args, **kwargs)
        self.parser_function = parser_function

    def clean(self, value):
        value = super(SignatureFormField, self).clean(value)
        try:
            self.parser_function(value)
        except Exception, e:
            raise forms.ValidationError(e)
        return value

        
class SignatureField(models.TextField):

    description = 'Signature for a variable. Ex, InterfaceName varName'

    def __init__(self, parser_function, multiline=False, *args, **kwargs):
        super(SignatureField, self).__init__(*args, **kwargs)
        self.parser_function = parser_function
        self.multiline = multiline
        
    def formfield(self, **kwargs):
        defaults = {'form_class': SignatureFormField}
        defaults.update(kwargs)
        defaults['widget'] = self.multiline and forms.Textarea or forms.TextInput
        defaults['parser_function'] = self.parser_function
        return super(SignatureField, self).formfield(**defaults)


class IdentifierField(models.CharField):

    description = ''
    
    def __init__(self, *args, **kwargs):
        _kwargs = {'max_length': 200, 'unique': True}
        _kwargs.update(kwargs)
        super(IdentifierField, self).__init__(*args, **_kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.RegexField,
            'regex': r'^[A-Za-z_][A-Za-z_0-9]*$',
            'error_messages': {'invalid': 'An identifier starts with a letter or underscore, and continues with letters, underscores, or numbers'},
            }
        defaults.update(kwargs)
        
        return super(IdentifierField, self).formfield(**defaults)
