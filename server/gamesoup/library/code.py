'''
Helpers for working with type code.
'''


import re


class TypeCode(object):
    
    pattern = {
        'interface-methods-header': re.compile(r'/\*\s*Interface Methods\s*\*/', re.IGNORECASE),
        'engine-hooks-header': re.compile(r'/\*\s*Engine Hooks\s*\*/', re.IGNORECASE),
        'implementation-header': re.compile(r'/\*\s*Implementation Methods\s*\*/', re.IGNORECASE),
        'method': re.compile(r'/\* vVv \*/\s*(?P<method_name>[A-Za-z0-9_]+)\s*\:\s*function\([,A-Za-z0-9_ ]*\)\s*\{\s*(?P<method_body>.*?)\s*\}\,?\s*/\* \^A\^ \*/', re.MULTILINE | re.DOTALL),
        'implementation': re.compile(r'gamesoup\.library\.types\.[A-Za-z0-9_]+\.addMethods\(\{\s*(?P<implementation>.*?)\s*\}\);\Z', re.MULTILINE | re.DOTALL),
    }
    
    def __init__(self, type):
        self._type = type
        self._code = self._parse(type.code)

    def _parse(self, w):
        '''
        Parse Type#code and store customized sections.
        '''
        self._interface_method = {}
        self._engine_hook = {}
        self._implementation = None
        imh_match = self.pattern['interface-methods-header'].search(w)
        ehh_match = self.pattern['engine-hooks-header'].search(w)
        ih_match = self.pattern['implementation-header'].search(w)
        
        def collect(c, x):
            m = self.pattern['method'].search(x)
            while m:
                d = m.groupdict()
                c[d['method_name']] = d['method_body']
                x = x[m.end(0):]
                m = self.pattern['method'].search(x)
        
        # Interface
        if imh_match:
            end = (ehh_match and ehh_match.start(0)) \
                or (ih_match and ih_match.start(0))
            collect(self._interface_method, w[imh_match.end(0):end])
                
        # Engine hooks
        if ehh_match:
            end = ih_match and ih_match.start(0)
            collect(self._engine_hook, w[ehh_match.end(0):end])
        
        # Implemenation
        if ih_match:
            m = self.pattern['implementation'].search(w[ih_match.end(0):])
            self._implementation = m.groupdict()['implementation']

    def interface_method(self, method_name):
        return self._interface_method.get(method_name, '')
    
    def engine_hook(self, hook_name):
        return self._engine_hook.get(hook_name, '')

    def implementation(self):
        return self._implementation

    def __unicode__(self):
        return u'%s\n%s\n%s' % (self._interface_method, self._engine_hook, self._implementation)
