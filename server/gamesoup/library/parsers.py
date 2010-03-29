import re
from cStringIO import StringIO
from gamesoup.library.errors import *
from gamesoup.library.templation import InterfaceExpression


patterns = {'id': '[A-Za-z_][A-Za-z_0-9]*'}
patterns['ta'] = '%(id)s\s*=\s*%(id)s' % patterns
patterns['tas'] = '\<\s*%(ta)s(?:\s*,\s*%(ta)s)*\s*\>' % patterns
patterns['interface_expression_chars'] = r'[A-Za-z0-9_<>=, ]+'


def parse_type_signature(signature):
    '''
    Convert from encoded signature to dictionary object.

    Example,
        """
        I1 param1
        I2 param2
        """
    to
        {
            "parameters": [p1, p2],
        }
    '''
    from gamesoup.library.models import Variable
    sigs = [sig.strip() for sig in signature.split('\n') if sig.strip()]
    d = {
        'parameters': map(Variable.objects.for_signature, sigs),
    }
    return d


def parse_method_signature(signature):
    '''
    Convert from encoded signature to dictionary object.
    
    Example,
        "I3 methodName(I1 p1, I2 p2)"
    to
        {
            "returned": Variable(interface=I3),
            "name": "methodName",
            "parameters": [Variable(interface=I1, name="p1"), Variable(interface=I2, name="p2")],
        }
        
    Example,
        "methodName()"
    to
        {
            "returned": Variable(interface=Nothing),
            "name": "methodName",
            "parameters": [],
        }
    '''
    from gamesoup.library.models import Variable
    p = re.compile(r'^\s*(?:(?P<return_type_name>%(id)s)\s+)?(?P<name>%(id)s)\s*\((?P<arg_sigs>[^)]*)\)\s*$' % patterns)
    signature = signature.strip()
    m = p.match(signature.strip())
    if not m:
        raise SignatureParseError('Invalid format for method signature: %s' % signature)
    d = m.groupdict()
    d['return_type_name'] = d['return_type_name'] or 'Nothing'
    d['returned'] = Variable.objects.for_signature('%(return_type_name)s returned' % d)
    sigs = [sig.strip() for sig in d['arg_sigs'].strip().split(',') if sig.strip()]
    d['parameters'] = map(Variable.objects.for_signature, sigs)
    del d['return_type_name']
    del d['arg_sigs']
    return d


def parse_variable_signature(signature):
    '''
    Convert from encoded signature to dictionary object.
    
    Example,
        "I1 varName"
    to
        {
            'name': 'varName',
            'interface_name': 'I1',
            'interface': I1,
            'template_arguments': None,
        }
    
    Example,
        "IDoesNotExist a"
    to
        {
            "name": "a",
            "interface_name": 'IDoesNotExist',
            "interface": None,
            "template_arguments": None,
        }
    
    Example,
        "Visitor<Item=I2> visitor"
    to
        {
            "name": "visitor",
            "interface_name": "Visitor",
            "interface": Visitor,
            "template_arguments": "<Item=I2>",
        }
    '''        
    from gamesoup.library.models import Interface
    p = re.compile(r'^\s*(?P<interface_expression>%(interface_expression_chars)s?)\s+(?P<name>%(id)s)\s*$' % patterns)
    m = p.match(signature)
    if not m:
        raise SignatureParseError('Invalid format for variable signature: %s' % signature)
    d = m.groupdict()
    try:
        exp = InterfaceExpression(d['interface_expression'])
    except Exception:
        raise SignatureParseError('Invalid format for interface expression: %s' % d['interface_expression'])
    del d['interface_expression']
    d['interface'] = exp.interface
    d['interface_name'] = exp.interface_name
    d['template_arguments'] = exp.template_arguments
    return d
