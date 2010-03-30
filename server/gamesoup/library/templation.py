'''
Provides functions and classes for working with Interface expressions,
which are the backbone of templated interfaces and types.
'''


import re
import sys


__all__ = (
    'InterfaceExpression',
    )


class InterfaceExpression(object):
    
    '''
    An interface expression is a way of concisely specifying
    binds of interface template parameters. These expressions
    can be used to determine compatibility relations. Two
    expressions a and b can relate to each other in these ways:
    
        a  < b    a is tighter than b
        a  > b    a is looser than b
        a == b    a is the same as b
        a != b    a is incompatible with b
    '''
    
    def __init__(self, expr_text, load_interface=True):
        from gamesoup.library.models import Interface
        self._expr_text = str(expr_text)
        self._ident, self._args_text = self._parse_a(expr_text)
        self._args = []
        self.is_fake = False
        if self._args_text:
            self._args = [
                    (k,InterfaceExpression(v, load_interface=load_interface)) 
                    for k,v
                    in self._parse_b(self._args_text)
                    ]
        self._argdict = dict(self._args)
        if load_interface:
            try:
                self._interface = Interface.objects.get(name=self._ident)
                self._interfaces = [self._interface]
            except Interface.DoesNotExist:
                # The interface must be a template parameter
                self._interface = None
                self._interfaces = []
                self.is_fake = True

    def get_is_built_in(self):
        return len(self._interfaces) == 1 and self._interfaces[0].is_built_in
    is_built_in = property(get_is_built_in)

    def get_interface(self):
        return self._interface
    interface = property(get_interface)

    def get_interfaces(self):
        return self._interfaces
    interfaces = property(get_interfaces)
    
    def get_interface_name(self):
        return self._ident
    interface_name = property(get_interface_name)

    def get_template_arguments(self):
        if not self._args:
            return None
        else:
            return '<%s>' % ','.join(['%s=%s' % (k, v) for k,v in self._args])
    template_arguments = property(get_template_arguments)

    def compare(self, template_param):
        arg = self[template_param]
        weakest = self._interface.template_parameters.get(name=template_param).weakest
        return '%r < %s' % (arg, weakest)

    def same_as(self, other):
        return `self` == `other`

    def tighter_than(self, other):
        from gamesoup.library.models import Interface
        if self.interface.is_built_in or other.interface.is_built_in:
            if other.interface == Interface.objects.any():
                return True
            else:
                return False            
        a = self.interface
        b = other.interface
        for method in other.interface.methods.all():
            if self.interface.methods.filter(pk=method.id).count() == 0:
                return False
        for template_param, other_expr in other._argdict.items():
            try:
                expr = self._argdict[template_param]
            except KeyError:
                tp = self.interface.template_parameters.get(name=template_param)
                expr = InterfaceExpression(tp.weakest)
            if other_expr.tighter_than(expr) or not (expr.tighter_than(other_expr) or expr.same_as(other_expr)):
                return False
        return True
        
    def __eq__(self, other): return self.same_as(other)
    def __lt__(self, other): return self.tighter_than(other)
    def __gt__(self, other): return other.tighter_than(self)

    def __getitem__(self, template_param):
        return self._argdict[template_param]

    def __repr__(self):
        if self.is_fake:
            w = '%%(%s)s' % self._ident
        else:
            w = self._ident
        if self._args:
            w += '<'
            w += ','.join([
                '%s=%s' % (k, `v`)
                for k,v
                in self._args
                ])
            w += '>'
        return w        

    @staticmethod
    def _parse_a(w):
        global patterns
        if not w.strip():
            return 'Nothing', ''
        m = patterns['interface_expression'].match(w)
        if not m:
            raise ValueError('Cannot parse interface expression')
        d = m.groupdict()
        args = d['arguments']
        return d['identifier'], args and args.replace(' ', '') or None

    @staticmethod
    def _parse_b(w):
        global patterns
        args = []
        while w:
            i = w.find('=')      
            j = InterfaceExpression._next_arg(w)
            if j == -1: j = len(w)
            args.append((w[:i], w[i+1:j]))
            w = w[j+1:]
        return args
    
    @staticmethod
    def _next_arg(w):
        global patterns
        m = re.match(r'^(%(identifier)s\=%(identifier)s).*$' % patterns, w)
        if not m or m.end(1) == len(w):
            return -1
        i = m.end(1)
        if w[i] != '<':
            return w.find(',')
        brackets = 1
        while brackets > 0 and i < len(w) - 1:
            i += 1
            if w[i] == '<':
                brackets += 1
            elif w[i] == '>':
                brackets -= 1
        j = w[i:].find(',')
        if j == -1:
            return -1
        else:
            return i + j
        

patterns = {
    'identifier': r'[A-Za-z_][A-Za-z_0-9]*',
    'arg_chars': r'[A-Za-z_0-9=<>, ]+?',
    }
patterns['interface_expression'] = re.compile(r'^\s*(?P<identifier>%(identifier)s)\s*(?:\<\s*(?P<arguments>%(arg_chars)s)\s*\>)?\s*$' % patterns)
patterns['next_argument'] = re.compile(r'(?P<identifier>%(identifier)s)\=(?P<expr>.*)(?P<rest>.*)$' % patterns)


__test__ = {'doctest': """
>>> from gamesoup.library.templation import InterfaceExpression as Expr

>>> Expr._parse_a('foo')
('foo', None)

>>> Expr._parse_a('foo<bar=car>')
('foo', 'bar=car')

>>> Expr._parse_a('  foo  <  bar = car  >  ')
('foo', 'bar=car')

>>> Expr._parse_a('foo< bar=car, cat = bat, bunch=munch> ')
('foo', 'bar=car,cat=bat,bunch=munch')

>>> Expr._parse_a('foo<bar=foo<bar=cat>>')
('foo', 'bar=foo<bar=cat>')

>>> Expr._next_arg('')
-1

>>> Expr._next_arg('bar=car')
-1

>>> Expr._next_arg('bar=car,bat=cat')
7

>>> Expr._next_arg('bar=foo<bar=cat,bunch=munch>,hoot=boot')
28

>>> Expr._next_arg('bar=foo<bar=foo<bar=car,wish=fish>,bunch=munch>,hoot=boot')
47

>>> Expr._parse_b('bar=car')
[('bar', 'car')]

>>> Expr._parse_b('bar=car,bat=cat')
[('bar', 'car'), ('bat', 'cat')]

>>> Expr._parse_b('bar=foo<bar=cat,bunch=munch>')
[('bar', 'foo<bar=cat,bunch=munch>')]

>>> Expr('Foo', load_interface=False)
Foo

>>> Expr('Foo<Bar=Car>', load_interface=False)
Foo<Bar=Car>

>>> Expr('Foo<Bar=Foo<Bar=Foo<Bar=Car,Wish=Fish>,Bunch=Munch>,Hoot=Boot>', load_interface=False)
Foo<Bar=Foo<Bar=Foo<Bar=Car,Wish=Fish>,Bunch=Munch>,Hoot=Boot>
"""
}
