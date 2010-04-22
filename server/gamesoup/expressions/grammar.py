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
                
ATOMIC_EXPR     ::= INTERFACE_ID
                |   INTERFACE_ID "<" ARG_LIST_PART ">"
                |   VARIABLE
                ;

VARIABLE        ::= INTERFACE_ID "." VARIABLE_ID
                |   TYPE_ID "." VARIABLE_ID
                |   OBJECT_ID "." VARIABLE_ID
                ;
                
INTERFACE_ID    ::= /[A-Z][A-Za-z0-9_]*/ ;

VARIABLE_ID     ::= /[a-z][A-Za-z0-9_]*/ ;

BUILT_IN_ID     ::= /[A-Z][A-Za-z0-9_]*\!/ ;

TYPE_ID         ::= /\@[A-Z][A-Za-z0-9_]*/ ;

OBJECT_ID       ::= /[1-9][0-9]*/ ;

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
        'type_id': r'\@[A-Z][A-Za-z0-9_]*',
        'object_id': r'[1-9][0-9]*',
        'built_in_id': r'[A-Z][A-Za-z0-9_]*\!',
    }
    
    @staticmethod
    def expr(w):
        """
        >>> Rule.expr('Foo')
        ('EXPR', ('ATOMIC_EXPR', ('INTERFACE_ID', 'Foo')))
        
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
            pass
        try:
            return ('EXPR', Rule.built_in_id(w))
        except _E:
            pass
        raise _E('Could not parse %s as EXPR' % w)
    
    @staticmethod
    def atomic_expr(w):
        """
        >>> Rule.atomic_expr('Foo')
        ('ATOMIC_EXPR', ('INTERFACE_ID', 'Foo'))

        >>> Rule.atomic_expr('Foo<bar=Bar>')
        ('ATOMIC_EXPR', ('INTERFACE_ID', 'Foo'), ('ARG_LIST_PART', ('ARG', ('VARIABLE_ID', 'bar'), ('EXPR', ('ATOMIC_EXPR', ('INTERFACE_ID', 'Bar'))))))
        
        >>> Rule.atomic_expr('@Type.var')
        ('ATOMIC_EXPR', ('VARIABLE', ('TYPE_ID', '@Type'), ('VARIABLE_ID', 'var')))

        >>> Rule.atomic_expr('2.var')
        ('ATOMIC_EXPR', ('VARIABLE', ('OBJECT_ID', '2'), ('VARIABLE_ID', 'var')))

        >>> Rule.atomic_expr('Foo.var')
        ('ATOMIC_EXPR', ('VARIABLE', ('INTERFACE_ID', 'Foo'), ('VARIABLE_ID', 'var')))
        """
        m = re.match(r'^\s*(%(interface_id)s)\s*(?:\<\s*(.*?)\s*\>)?\s*$' % Rule.lex, w)
        if m:
            if m.group(2):
                return ('ATOMIC_EXPR', Rule.interface_id(m.group(1)), Rule.arg_list_part(m.group(2)))
            else:
                return ('ATOMIC_EXPR', Rule.interface_id(m.group(1)))
        try:
            return ('ATOMIC_EXPR', Rule.variable(w))
        except _E:
            raise _E('Could not parse %s as ATOMIC_EXPR' % w)

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
    def variable(w):
        """
        >>> Rule.variable('@Type.var')
        ('VARIABLE', ('TYPE_ID', '@Type'), ('VARIABLE_ID', 'var'))

        >>> Rule.variable('2.var')
        ('VARIABLE', ('OBJECT_ID', '2'), ('VARIABLE_ID', 'var'))

        >>> Rule.variable('Foo.var')
        ('VARIABLE', ('INTERFACE_ID', 'Foo'), ('VARIABLE_ID', 'var'))
        """
        m = re.match(r'^\s*(%(type_id)s)\.(%(variable_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('VARIABLE', Rule.type_id(m.group(1)), Rule.variable_id(m.group(2)))
        m = re.match(r'^\s*(%(object_id)s)\.(%(variable_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('VARIABLE', Rule.object_id(m.group(1)), Rule.variable_id(m.group(2)))
        m = re.match(r'^\s*(%(interface_id)s)\.(%(variable_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('VARIABLE', Rule.interface_id(m.group(1)), Rule.variable_id(m.group(2)))
        raise _E('Could not parse %s as VARIABLE' % w)
        
    @staticmethod
    def interface_id(w):
        """
        >>> Rule.interface_id('Foo')
        ('INTERFACE_ID', 'Foo')
        """
        m = re.match(r'^\s*(%(interface_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('INTERFACE_ID', m.group(1))
        raise _E('Could not parse %s as INTERFACE_ID' % w)

    @staticmethod
    def variable_id(w):
        """
        >>> Rule.variable_id('foo')
        ('VARIABLE_ID', 'foo')
        """
        m = re.match(r'^\s*(%(variable_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('VARIABLE_ID', m.group(1))
        raise _E('Could not parse %s as VARIABLE_ID' % w)    

    @staticmethod
    def type_id(w):
        """
        >>> Rule.type_id('@Foo')
        ('TYPE_ID', '@Foo')
        """
        m = re.match(r'^\s*(%(type_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('TYPE_ID', m.group(1))
        raise _E('Could not parse %s as TYPE_ID' % w)

    @staticmethod
    def object_id(w):
        """
        >>> Rule.object_id('12')
        ('OBJECT_ID', '12')
        """
        m = re.match(r'^\s*(%(object_id)s)\s*$' % Rule.lex, w)
        if m:
            return ('OBJECT_ID', m.group(1))
        raise _E('Could not parse %s as OBJECT_ID' % w)
    
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
            return ('ARG', Rule.variable_id(m.group(1)), Rule.expr(m.group(2)))
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
