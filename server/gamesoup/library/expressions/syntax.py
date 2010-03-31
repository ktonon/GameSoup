'''
For parsing interface expressions.

The grammar rules are:

EXPR            ::= ATOMIC_EXPR
                |   EXPR_LIST
                ;
                
EXPR_LIST       ::= "[" EXPR_LIST_PART "]" ;
                
EXPR_LIST_PART  ::= ATOMIC_EXPR
                |   ATOMIC_EXPR "&" EXPR_LIST_PART
                ;
                
ATOMIC_EXPR     ::= ID
                |   INTERFACE_ID "<" ARG_LIST_PART ">"
                ;
                
ID              ::= INTERFACE_ID
                |   VARIABLE_ID
                ;

INTERFACE_ID    ::= /[A-Z][A-Za-z0-9_]*/ ;

VARIABLE_ID     ::= /[a-z][A-Za-z0-9_]*/ ;

ARG_LIST_PART   ::= ARG
                |   ARG "," ARG_LIST_PART
                ;

ARG             ::= VARIABLE_ID "=" EXPR ;

'''

import re
import sys


__all__ = (
    'parse_interface_expression',
    )


class InterfaceExpressionParseError(ValueError): pass
_E = InterfaceExpressionParseError


def parse_interface_expression(w):
    tree = Rule.expr(w)
    return Expression(tree)


class Expression(object):
    '''
    An interface expression is a way of concisely specifying
    interfaces which are compositions. Interfaces are composed
    by binding one interface to the template parameter of another.
    
    This class accepts an interface expression (which is a string)
    and parses it into an intermediate data structure.
    '''
    
    def __init__(self, tree):
        '''
        Parse an interface expression expr_text.
        '''
        assert tree[0] == 'EXPR'
        self._atomics = []
        if tree[1][0] == 'ATOMIC_EXPR':
            self._atomics.append(AtomicExpression(tree[1]))
        else:
            assert tree[1][0] == 'EXPR_LIST'
            x = tree[1][1]
            while x:
                self._atomics.append(AtomicExpression(x[1]))
                x = len(x) > 2 and x[2] or None
        
    def __repr__(self):
        if len(self._atomics) == 1:
            return `self._atomics[0]`
        else:
            return '[%s]' % ' & '.join([`a` for a in self._atomics])

    def _get_atomics(self):
        return self._atomics
    atomics = property(_get_atomics)


class AtomicExpression(object):
    
    def __init__(self, tree):
        assert tree[0] == 'ATOMIC_EXPR', 'Found %s' % tree[0]
        assert tree[1][0] == 'ID', 'Found %s' % tree[1][0]
        assert tree[1][1][0] in ('INTERFACE_ID', 'VARIABLE_ID'), 'Found %s' % tree[1][1][0]
        self._identifier = tree[1][1][1]
        self._is_variable = tree[1][1][0] == 'VARIABLE_ID'
        self._args = []
        if len(tree) > 2:
            x = tree[2]
            assert x[0] == 'ARG_LIST_PART'
            while x:
                self._args.append(Argument(x[1]))
                x = len(x) > 2 and x[2] or None

    def __repr__(self):    
        w = self._identifier
        if self._args:
            w += '<%s>' % ', '.join([`arg` for arg in self._args])
        return w

    def _is_variable(self):
        return self._is_variable
    is_variable = property(_is_variable)

    def _get_identifier(self):
        return self._identifier
    identifier = property(_get_identifier)

    def _get_arguments(self):
        return self._args
    arguments = property(_get_arguments)

    def __getitem__(self, template_param):
        return self._argdict[template_param]


class Argument(object):
    
    def __init__(self, tree):
        assert tree[0] == 'ARG', 'Found %s' % tree[0]
        assert tree[1][0] == 'ID', 'Found %s' % tree[1][0]
        assert tree[1][1][0] == 'VARIABLE_ID', 'Found %s' % tree[1][1][0]
        assert tree[2][0] == 'EXPR'
        self._variable_id = tree[1][1][1]
        self._expr = Expression(tree[2])

    def __repr__(self):
        return '%s=%s' % (self._variable_id, `self._expr`)

    def _get_identifier(self):
        return self._variable_id
    identifier = property(_get_identifier)
    
    def _get_expression(self):
        return self._expr
    expression = property(_get_expression)


class Rule(object):
    
    lex = {
        'interface_id': r'[A-Z][A-Za-z0-9_]*',
        'variable_id': r'[a-z][A-Za-z0-9_]*',
    }
    
    @staticmethod
    def expr(w):
        try:
            return ('EXPR', Rule.atomic_expr(w))
        except _E:
            return ('EXPR', Rule.expr_list(w))
    
    @staticmethod
    def atomic_expr(w):
        m = re.match(r'^\s*(%(interface_id)s)\s*\<\s*(.*?)\s*\>\s*$' % Rule.lex, w)
        if m:
            return ('ATOMIC_EXPR', Rule.id(m.group(1)), Rule.arg_list_part(m.group(2)))
        return ('ATOMIC_EXPR', Rule.id(w))

    @staticmethod
    def expr_list(w):
        m = re.match(r'^\s*\[\s*(.*)\s*\]\s*$', w)
        if m:
            return ('EXPR_LIST', Rule.expr_list_part(m.group(1)))
        raise _E('Could not parse %s as EXPR_LIST' % w)
    
    @staticmethod
    def expr_list_part(w):
        for i in allindices(w, '&'):
            try:
                return ('EXPR_LIST_PART', Rule.atomic_expr(w[:i]), Rule.expr_list_part(w[i+1:]))
            except _E:
                pass # Keep trying
        # Try parsing as an atomic expression
        return ('EXPR_LIST_PART', Rule.atomic_expr(w))
    
    @staticmethod
    def id(w):
        m = re.match(r'^\s*(%(interface_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('ID', ('INTERFACE_ID', m.group(1)))
        m = re.match(r'^\s*(%(variable_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('ID', ('VARIABLE_ID', m.group(1)))
        raise _E('Could not parse %s as ID' % w)
    
    @staticmethod
    def arg_list_part(w):
        for i in allindices(w, ','):
            try:
                return ('ARG_LIST_PART', Rule.arg(w[:i]), Rule.arg_list_part(w[i+1:]))
            except _E:
                pass # Keep trying
        # Try parsing as a simple arg
        return ('ARG_LIST_PART', Rule.arg(w))
    
    @staticmethod
    def arg(w):
        m = re.match(r'^\s*(%(variable_id)s)\s*\=\s*(.*?)\s*$' % Rule.lex, w)
        if m:
            return ('ARG', Rule.id(m.group(1)), Rule.expr(m.group(2)))
        raise _E('Could not parse %s as ARG' % w)    


def allindices(string, sub, listindex=None, offset=0):
    listindex = listindex or []
    if (string.find(sub) == -1):
        return listindex
    else:
        offset = string.index(sub)+offset
        listindex.append(offset)
        string = string[(string.index(sub)+1):]
        return allindices(string, sub, listindex, offset+1)



__test__ = {'doctest': """
>>> from gamesoup.library.expressions.syntax import parse_interface_expression as parse
>>> from gamesoup.library.expressions.syntax import allindices, Rule

>>> allindices('abc', ',')
[]

>>> allindices('a,b,c', ',')
[1, 3]

>>> Rule.id('Foo')
('ID', ('INTERFACE_ID', 'Foo'))

>>> Rule.id('foo')
('ID', ('VARIABLE_ID', 'foo'))

>>> Rule.atomic_expr('Foo')
('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Foo')))

>>> Rule.atomic_expr('Foo<bar=Bar>')
('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Foo')), ('ARG_LIST_PART', ('ARG', ('ID', ('VARIABLE_ID', 'bar')), ('EXPR', ('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Bar')))))))

>>> Rule.expr('Foo')
('EXPR', ('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Foo'))))

>>> parse('Foo')
Foo

>>> parse(' [ Foo&Bar ] ')
[Foo & Bar]

>>> parse('Foo<bar=Bar>')
Foo<bar=Bar>

>>> parse(' Foo < bar  = Bar  , car = Car > ')
Foo<bar=Bar, car=Car>

>>> parse('Foo<bar=[Bar&Car]>')
Foo<bar=[Bar & Car]>

>>> parse('Foo<bar=[Bar<far=Far,where=[Where&There]>&Car]>')
Foo<bar=[Bar<far=Far, where=[Where & There]> & Car]>

"""
}
