import re
from cStringIO import StringIO
from gamesoup.library.errors import *


patterns = {
    'id': '[A-Za-z_][A-Za-z_0-9]*',
    }


def parse_type_signature(signature):
    '''
    Convert from encoded signature to dictionary object.

    Example,
        I1 param1
        I2 param2
    to
        {
            "parameters": [p1, p2],
        }
    '''
    from gamesoup.library.models import Variable
    sigs = signature.split('\n')
    d = {
        'parameters': map(Variable.objects.for_signature, filter(bool, sigs)),
    }
    return d


def parse_interface_signature(signature):
    '''
    Convert from encoded signature to dictionary object.

    Example,
        I3 methodName(I1 p1, I2 p2)
        I3 otherMethod()
    to
        {
            "methods": [m1, m2],
        }
    '''
    from gamesoup.library.models import Method
    sigs = signature.split('\n')
    d = {
        'methods': map(Method.objects.for_signature, filter(bool, sigs)),
    }
    return d


def parse_method_signature(signature):
    '''
    Convert from encoded signature to dictionary object.
    
    Example,
        I3 MethodName(I1 p1, I2 p2)
    to
        {
            "returned": v3,
            "name": "MethodName",
            "mode": method_modes.CLASS_METHOD,
            "parameters": [v1, v2],
        }
    '''
    from gamesoup.library.models import Variable
    p = re.compile(r'^\s*(?P<return_type_name>%(id)s)\s+(?P<name>%(id)s)\s*\((?P<arg_sigs>[^)]*)\)\s*$' % patterns)
    signature = signature.strip()
    m = p.match(signature.strip())
    if not m:
        raise SignatureParseError('Invalid format for method signature: %s' % signature)
    d = m.groupdict()
    d['returned'] = Variable.objects.for_signature('%(return_type_name)s returned' % d)
    sigs = [sig.strip() for sig in d['arg_sigs'].strip().split(',')]
    d['parameters'] = map(Variable.objects.for_signature, filter(bool, sigs))
    return d


def parse_variable_signature(signature):
    '''
    Convert from encoded signature to dictionary object.
    
    Example,
        InterfaceName varName
    to
        {
            'name': 'varName',
            'interface_name': 'InterfaceName',
            'interface': SomeInterfaceObject,
        }
    '''        
    from gamesoup.library.models import Interface
    p = re.compile(r'^\s*(?P<interface_name>%(id)s)\s+(?P<name>%(id)s)\s*$' % patterns)
    m = p.match(signature)
    if not m:
        raise SignatureParseError('Invalid format for variable signature: %s' % signature)
    d = m.groupdict()
    try:
        d['interface'] = Interface.objects.get(name=d['interface_name'])
    except Interface.DoesNotExist:
        raise Interface.DoesNotExist('Interface with name "%s" referenced in variable signature "%s" does not exist.' % (d['interface_name'], signature))
    return d
