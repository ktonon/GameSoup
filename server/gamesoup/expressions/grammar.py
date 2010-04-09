'''
For parsing interface expressions.

The grammar rules are:

EXPR            ::= ATOMIC_EXPR
                |   EXPR_LIST
                |   BUILT_IN_ID
                ;

EXPR_LIST       ::= "[" EXPR_LIST_PART "]"
                |   "[" "]"
                ;
                
EXPR_LIST_PART  ::= ATOMIC_EXPR
                |   ATOMIC_EXPR "+" EXPR_LIST_PART
                ;
                
ATOMIC_EXPR     ::= ID
                |   INTERFACE_ID "<" ARG_LIST_PART ">"
                ;
                
ID              ::= INTERFACE_ID
                |   VARIABLE_ID
                ;

INTERFACE_ID    ::= /[A-Z][A-Za-z0-9_]*/ ;

VARIABLE_ID     ::= /[a-z][A-Za-z0-9_]*/ ;

BUILT_IN_ID     ::= /[A-Z][A-Za-z0-9_]*\!/ ;

ARG_LIST_PART   ::= ARG
                |   ARG "," ARG_LIST_PART
                ;

ARG             ::= VARIABLE_ID "=" EXPR ;

'''


import re


class Rule(object):
    
    lex = {
        'interface_id': r'[A-Z][A-Za-z0-9_]*',
        'variable_id': r'[a-z][A-Za-z0-9_]*',
        'built_in_id': r'[A-Z][A-Za-z0-9_]*\!',
    }
    
    @staticmethod
    def expr(w):
        """
        >>> Rule.expr('Foo')
        ('EXPR', ('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Foo'))))
        
        >>> Rule.expr('Foo!')
        ('EXPR', ('BUILT_IN_ID', 'Foo!'))
        """
        try:
            return ('EXPR', Rule.atomic_expr(w))
        except _E:
            pass
        try:
            return ('EXPR', Rule.expr_list(w))
        except _E:
            return ('EXPR', Rule.built_in_id(w))
    
    @staticmethod
    def atomic_expr(w):
        """
        >>> Rule.atomic_expr('Foo')
        ('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Foo')))

        >>> Rule.atomic_expr('Foo<bar=Bar>')
        ('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Foo')), ('ARG_LIST_PART', ('ARG', ('ID', ('VARIABLE_ID', 'bar')), ('EXPR', ('ATOMIC_EXPR', ('ID', ('INTERFACE_ID', 'Bar')))))))
        """
        m = re.match(r'^\s*(%(interface_id)s)\s*\<\s*(.*?)\s*\>\s*$' % Rule.lex, w)
        if m:
            return ('ATOMIC_EXPR', Rule.id(m.group(1)), Rule.arg_list_part(m.group(2)))
        return ('ATOMIC_EXPR', Rule.id(w))

    @staticmethod
    def expr_list(w):
        m = re.match(r'^\s*\[\s*(.*)\s*\]\s*$', w)
        if m:
            content = m.group(1)
            if content:
                return ('EXPR_LIST', Rule.expr_list_part(m.group(1)))
            else:
                return ('EXPR_LIST',)
        raise _E('Could not parse %s as EXPR_LIST' % w)
    
    @staticmethod
    def expr_list_part(w):
        for i in allindices(w, '+'):
            try:
                return ('EXPR_LIST_PART', Rule.atomic_expr(w[:i]), Rule.expr_list_part(w[i+1:]))
            except _E:
                pass # Keep trying
        # Try parsing as an atomic expression
        return ('EXPR_LIST_PART', Rule.atomic_expr(w))
    
    @staticmethod
    def id(w):
        """
        >>> Rule.id('Foo')
        ('ID', ('INTERFACE_ID', 'Foo'))

        >>> Rule.id('foo')
        ('ID', ('VARIABLE_ID', 'foo'))
        """
        m = re.match(r'^\s*(%(interface_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('ID', ('INTERFACE_ID', m.group(1)))
        m = re.match(r'^\s*(%(variable_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('ID', ('VARIABLE_ID', m.group(1)))
        raise _E('Could not parse %s as ID' % w)
    
    @staticmethod
    def built_in_id(w):
        """
        >>> Rule.built_in_id('Foo!')
        ('BUILT_IN_ID', 'Foo!')
        """
        m = re.match(r'^\s*(%(built_in_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('BUILT_IN_ID', m.group(1))
        raise _E('Could not parse %s as BUILT_IN_ID' % w)

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


class ExprParseError(ValueError): pass
_E = ExprParseError


def allindices(w, x):
    '''
    Find indices of all occurence of x in w.
    Meant to be used as an iterator.
    
    >>> list(allindices("abc", ","))
    []
    
    >>> list(allindices("a,bc,d,ef,g", ","))
    [1, 4, 6, 9]
    '''
    i, c = w.find(x) + 1, -1
    while i:
        c += i
        i = w[c+1:].find(x) + 1
        yield c


__test__ = {'doctest': """
You should not be able to make unions with built in interfaces.

    >>> try:
    ...     Rule.expr('[Foo! + Bar]')
    ... except Exception:
    ...     print 'Failed'
    Failed
    
"""}
