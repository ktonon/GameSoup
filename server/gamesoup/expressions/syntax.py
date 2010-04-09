'''
For parsing interface expressions.
'''

import re
import sys
from gamesoup.expressions.grammar import Rule


__all__ = (
    'Expr',
    )


class Cached(object):
    
    @classmethod
    def unique(cls, obj):
        if not hasattr(cls, '_cache'): cls._cache = {}
        rep = `obj`
        cached_obj = cls._cache.get(rep, None)
        if cached_obj is None:
            cached_obj = obj
            cls._cache[rep] = cached_obj
        return cached_obj



class Expr(Cached):
    '''
    This class accepts an interface expression (which is a string)
    and parses it into an intermediate data structure.
    '''
    
    ###############################################################################
    # Instantiation
    
    @classmethod
    def parse(cls, w):
        """
        This is the usual way to instantiate an interface expression
        from a string.
        
        The most basic interface expression is the empty expression,
        to which all other expressions are super. It is represented
        as an empty union set using square brackets.
        
            >>> Expr.parse('[]')
            []
        
        Parsing an empty string will just return the integer 0
        instead of an expression object.
        
            >>> nothing = Expr.parse('')
            >>> nothing
            0
            >>> nothing.__class__.__name__
            'int'
        """
        if re.match(r'^\s*(?:0)?\s*$', w): return 0
        tree = Rule.expr(w)
        return cls.from_tree(tree)
        
    @classmethod
    def from_tree(cls, tree):
        assert tree[0] == 'EXPR'
        atoms = []
        if tree[1][0] in ('ATOMIC_EXPR', 'BUILT_IN_ID'):
            atoms.append(Atom.from_tree(tree[1]))
        else:
            assert tree[1][0] == 'EXPR_LIST'
            if len(tree[1]) > 1:
                x = tree[1][1]
                while x:
                    atoms.append(Atom.from_tree(x[1]))
                    x = len(x) > 2 and x[2] or None
        return cls.from_atoms(atoms)
        
    @classmethod
    def from_atoms(cls, atoms):
        '''
        Create an expression from a sequence of atoms.
        '''
        expr = cls()
        expr._child = dict([(atom.id, atom) for atom in atoms])
        return cls.unique(expr)
    
    ###############################################################################
    # Queries
    
    def _get_sorted_atoms(self):
        """
        >>> e = Expr.parse('[D + B + C + A]')
        >>> e.atoms
        [A, B, C, D]
        
        >>> e.atoms[0].__class__.__name__
        'Atom'
        """
        return sorted(self._child.values(), cmp=cmp_by_id)
    atoms = property(_get_sorted_atoms)
        
    def _get_sorted_ids(self):
        """
        >>> Expr.parse('[D + B + C + A]').ids
        ['A', 'B', 'C', 'D']
        """
        return sorted([atom.id for atom in self._child.values()])
    ids = property(_get_sorted_ids)
    
    def _is_singleton(self):
        """
        >>> Expr.parse('[A]').is_singleton
        True
        
        >>> Expr.parse('A!').is_singleton
        True
        
        >>> Expr.parse('[a]').is_singleton
        True

        >>> Expr.parse('[A<item=B>]').is_singleton
        True
        
        >>> Expr.parse('[A + B]').is_singleton
        False
        """
        return len(self) == 1
    is_singleton = property(_is_singleton)
    
    def _is_built_in(self):
        """
        >>> Expr.parse('A').is_built_in
        False
        
        >>> Expr.parse('a').is_built_in
        False
        
        >>> Expr.parse('A!').is_built_in
        True
        
        >>> Expr.parse('[A<item=A!>]').is_built_in
        False
        """
        return self.is_singleton and self.singleton.is_built_in
    is_built_in = property(_is_built_in)
    
    def _is_var(self):
        """
        >>> Expr.parse('A').is_var
        False

        >>> Expr.parse('A!').is_var
        False

        >>> Expr.parse('a').is_var
        True

        >>> Expr.parse('[a]').is_var
        True

        >>> Expr.parse('[a + B]').is_var
        False
        """
        return self.is_singleton and self.singleton.is_var
    is_var = property(_is_var)
    
    def get_singleton(self):
        assert self.is_singleton
        return self.atoms[0]
    singleton = property(get_singleton)
    
    def __repr__(self):
        """
        Produce the normalized representation of this expression.
        For each level of nesting, all identifiers will be sorted
        alphabetically. White space is also normalized.

        Normal singleton interfaces and variables are placed within
        square brackets, to indicate that they can be unioned with
        other expressions.
        
            >>> Expr.parse('A')
            [A]
        
            >>> Expr.parse('a')
            [a]
        
        Built-in interfaces cannot be unioned with other interfaces,
        so they are represented outside of any square brackets.
        
            >>> Expr.parse('A!')
            A!
        """
        if self.is_built_in:
            return `self.singleton`
        return '[%s]' % ' + '.join([`a` for a in self.atoms])
    
    def __len__(self):
        """
        >>> len(Expr.parse('[]'))
        0
        
        >>> len(Expr.parse('A'))
        1

        >>> len(Expr.parse('A!'))
        1
        
        >>> len(Expr.parse('[A<item=[P+Q+R]> + B]'))
        2        
        """
        return len(self._child)

    def __nonzero__(self):
        """
        So that expressions are always evaluated as True. This is useful in
        short-circuited boolean python expressions which first check that
        an expression is not None and then use some property.
        
        For example:
        
            >>> e = Expr.parse('[A]')
            >>> e and e.is_singleton
            True
        
        Note that even an empty expression evaluates to True:
        
            >>> bool(Expr.parse('[]'))
            True
        
        However the nothing expression, which is not even an
        expression, but 0, will evaluate to False:
        
            >>> bool(Expr.parse(''))
            False
        """
        return True

    ###############################################################################
    # Composition
    
    def __add__(self, other):
        '''
        >>> a = Expr.parse('[R + S<item=Foo<color=Red, favorite=Murphy>, engine=Electric> + T]')
        >>> b = Expr.parse('[S<item=[Bar + Foo<item=Car, favorite=Fred>]> + T + U]')
        >>> a + b
        [R + S<engine=[Electric], item=[Bar + Foo<color=[Red], favorite=[Fred + Murphy], item=[Car]>]> + T + U]
        '''
        union = []
        for atom1, atom2 in self.join(other):
            if atom1 and atom2 and atom1 != atom2:
                union.append(atom1 + atom2)
            else:
                union.append(atom1 or atom2)
        return Expr.from_atoms(union)

    ###############################################################################
    # Comparison

    def super(self, other):
        '''
        Is this expression a super expression of other?
        
        If so, any place other is required, this one will work too.
        '''
        for atom1, atom2 in self.join(other):
            if atom1 and atom2 and not atom1.super(atom2):
                return False
            if not atom1 and atom2:
                return False
        return True

    def resolve(self, other, resolvent=None):
        '''
        Resolve self to other.
        '''

    def join(self, other):
        return _join(self, other, '_child', 'ids')


class Atom(Cached):
    
    ###############################################################################
    # Instantiation
    
    @classmethod
    def from_tree(cls, tree):
        if tree[0] == 'ATOMIC_EXPR':
            assert tree[1][0] == 'ID'
            assert tree[1][1][0] in ('INTERFACE_ID', 'VARIABLE_ID')
            args = []
            if len(tree) > 2:
                x = tree[2]
                assert x[0] == 'ARG_LIST_PART'
                while x:
                    args.append(Arg.from_tree(x[1]))
                    x = len(x) > 2 and x[2] or None
            return cls.from_args(args, id=tree[1][1][1], is_var=tree[1][1][0] == 'VARIABLE_ID')
        else:
            assert tree[0] == 'BUILT_IN_ID'
            return cls.from_args([], id=tree[1], is_built_in=True)
    
    @classmethod
    def from_args(cls, args, id, is_var=False, is_built_in=False):
        atom = cls()
        atom._id = id
        atom._is_var = is_var
        atom._is_built_in = is_built_in
        atom._arg = dict([(arg.id, arg) for arg in args])
        return cls.unique(atom)

    ###############################################################################
    # Queries
    
    is_var = property(lambda self: self._is_var)
    id = property(lambda self: self._id)
    is_built_in = property(lambda self: self._is_built_in)
    
    def get_sorted_param_ids(self):
        return sorted(self._arg.keys())
    param_ids = property(get_sorted_param_ids)
    
    def get_sorted_args(self):
        return sorted(self._arg.values(), cmp=cmp_by_id)
    args = property(get_sorted_args)

    def __repr__(self):    
        w = self.id
        if self._arg:
            w += '<%s>' % ', '.join([`arg` for arg in self.args])
        return w

    def __len__(self):
        return len(self._arg)

    def __nonzero__(self):
        return True
    
    ###############################################################################
    # Composition
    
    def __add__(self, other):
        assert self.id == other.id
        assert self.is_var == other.is_var
        union = []
        for arg1, arg2 in self.join(other):
            if arg1 and arg2 and arg1 != arg2:
                union.append(arg1 + arg2)
            else:
                union.append(arg1 or arg2)
        return Atom.from_args(union, id=self.id, is_var=self.is_var)

    ###############################################################################
    # Comparison

    def super(self, other):
        for arg1, arg2 in self.join(other):
            if arg1 and arg2 and not arg1.expr.super(arg2.expr):
                return False
            if not arg1 and arg2:
                return False
        return True

    def join(self, other):
        return _join(self, other, '_arg', 'param_ids')


class Arg(Cached):
    
    ###############################################################################
    # Instantiation
    
    @classmethod
    def from_tree(cls, tree):
        assert tree[0] == 'ARG', 'Found %s' % tree[0]
        assert tree[1][0] == 'ID', 'Found %s' % tree[1][0]
        assert tree[1][1][0] == 'VARIABLE_ID', 'Found %s' % tree[1][1][0]
        assert tree[2][0] == 'EXPR'        
        expr = Expr.from_tree(tree[2])
        return cls.from_expr(expr, id=tree[1][1][1])

    @classmethod
    def from_expr(cls, expr, id):
        arg = cls()
        arg._id = id
        arg._expr = expr
        return cls.unique(arg)
    
    ###############################################################################
    # Queries
    
    id = property(lambda self: self._id)
    expr = property(lambda self: self._expr)

    def __repr__(self):
        return '%s=%s' % (self.id, `self.expr`)
        
    def __nonzero__(self):
        return True
    
    ###############################################################################
    # Composition
    
    def __add__(self, other):
        assert self.id == other.id
        expr = self.expr + other.expr
        return Arg.from_expr(expr, id=self.id)

    ###############################################################################
    # Comparison

    def __gt__(self, other):
        return True


def cmp_by_id(x, y):
    return cmp(x.id, y.id)


def _join(a, b, d, ids):
    for id in set(getattr(a, ids)) | set(getattr(b, ids)):
        yield getattr(a, d).get(id, None), getattr(b, d).get(id, None)


__test__ = {'doctest': """
>>> from gamesoup.expressions.syntax import Expr

>>> any = Expr.parse('[]')
>>> any
[]

>>> any + any
[]

>>> foo = Expr.parse('Foo')
>>> foo
[Foo]

>>> bi = Expr.parse('BuiltIn!')
>>> bi
BuiltIn!

>>> bi.is_built_in
True

>>> foo is any + foo
True

>>> foobar = Expr.parse(' [ Foo+Bar ] ')
>>> foobar
[Bar + Foo]

>>> foobar is foobar + foo
True

>>> foobar + Expr.parse('[Far + Car]')
[Bar + Car + Far + Foo]

>>> Expr.parse('Foo<bar=Bar>')
[Foo<bar=[Bar]>]

>>> Expr.parse(' Foo < bar  = Bar  , car = Car > ')
[Foo<bar=[Bar], car=[Car]>]

>>> Expr.parse('Foo<bar=[Bar+Car]>')
[Foo<bar=[Bar + Car]>]

>>> r = Expr.parse('Readable')
>>> w = Expr.parse('Writable')
>>> r.super(r)
True

>>> r.super(w)
False

>>> w.super(r)
False

>>> (r + w).super(w)
True

>>> (r + w).super(r)
True

>>> (r + w).super(w + r)
True

>>> rs = Expr.parse('Readable<item=String>')
>>> rs.super(r)
True

>>> r.super(rs)
False

>>> rs.super(r + w)
False

>>> (r + w).super(rs)
False

>>> c1 = Expr.parse('Foo<bar=[Bar<far=Far,where=[Where+There]>+Car]>')
>>> c1
[Foo<bar=[Bar<far=[Far], where=[There + Where]> + Car]>]

>>> c2 = Expr.parse('[Foo<bar=[Bar<far=[Far+War],where=[Here+There+Every+Where],at=Fat>+Car<item=Bitem>+Fat<hat=Cat>]>+Quick]')
>>> c2.super(c1)
True

>>> c1.super(c2)
False

>>> Expr.parse('Foo<item=Bar>').super(Expr.parse('Foo<item=[]>'))
True

Take for example, "Iterable<item=Readable<item=over>>". Here, the outer "item"
is an interface template parameter of the interface Iterable. It is bound to an 
expression which involves the type template parameter "over". "over" requires
a minimum interface, but that minimum interface is not specified here. It can be
found by looking up the type template parameter in the database.

A resolvent is a dictionary which maps type template parameter names to other expressions.
A resolvent can be applied to an expression to replace all occurences of each key with
their respective values, yielding a new expression which is super to the first.

Note that if expression a is super to expression b, in a strict sense (that is, they are
not the same expression), then there are fewer objects which will be able to satisfy that
expression.

An objects working expression is a combination of the expression of its type, and of
resolvents applied to it as a result of type parameter bindings. If an object is bound to
the type parameter of another object, then the working expression of the object must
be super to the working expression of the type parameter. If this is not already the case
then a resolvent may be applied to the working expression of the object. The only way
a resolvent can change an expression, is by binding type template parameters which are
themselves bound to interface template parameters.

However! Type template parameters are used in 2 places:
    1) To bind interface template parameters
    2) In type parameters

And this is where it gets complicated. When you bind a type template parameter in order
to change the interface of an object which instantiates it, you may also inadvertantly
change the expressions of the type parameters. The cascades to any objects bound to those
type parameters.

So, we have an algorithm for binding type objects to type parameters which is recursive.
It goes like this:

(1) > Is bindee.expr.super(binder.param.expr)?
        > Yes: Ok, you are good. Just bind it.
        > No: Is bindee.expr.resolvable_with(binder.param.expr)?
            > No: Ok, you cannot bind it. You are done.
            > Yes:
                > Get the resolvent r, that will make bindee.expr.super(binder.param.expr)
                > Any any keys in r mentioned in bindee.Type's parameters?
                    > No: Okay, no harm.
                    > Yes: Are any of the affected parameters already bound?
                        > In either case, you will also have to apply
                          the resolvent to each affected parameter.
                        > No: Okay, no harm.
                        > Yes: RECURSE: apply (1) to the bound object and the parameter.
                > Is bindee already bound to parameters of any other objects?
                    > No: Okay.
                    > Yes: RECURSE: apply (1) to bindee and each parameter to which
                      it is already bound. But, make sure you use bindee's working
                      expression as it would look AFTER applying the resolvent

Here is an example:

#     >>> obj = Expr.parse('Iterable<item=Readable<item=over>>')
#     >>> param = Expr.parse('Iterable<item=Readable<item=Clearable>>')
#     >>> resolvent = obj.resolvent_for(param)
#     >>> resolvent
#     {'over': [Clearable]}
# 
# Now say we lookup the minimum interface required by the type template parameter
# "over" and find it to be "[Drivable]". That's is no good, because:
# 
#     >>> Expr.parse('Clearable').super(Expr.parse('Drivable'))
#     False
# 
# 
# because after applying the resolvent:
# 
#     >>> obj_after = obj.apply_resolvent(resolvent)
#     >>> obj_after.super(param)
#     True
#     
# In order to get this algorithm implemented. I need to do the following:
# 
#     1)

I have a general purpose type called
    @List<item=[]>
which implements
    [Iterable<item=@List.item[]> + Stack<item=@List.item[]>]
    
Then I have
    @Copier<item=[]>
which implements
    [Action]
and has parameters
    src :   [Iterable<item=Readable<item=@Copier.item[]>>]
    dest:   [Stack<item=@Copier.item[]>]

A copier reads data from its source and pushes it onto its
destination.

I instantiate a @List object
    1   :   [Iterable<item=@List.item[]> + Stack<item=@List.item[]>]
and a @Copier object
    2   :   [Action]
        src :   [Iterable<item=Readable<item=@Copier.item[]>>]
        dest:   [Stack<item=@Copier.item[]>]

Note that
    1.expr.super(2.dest)
because

    >>> Expr.parse('[Iterable<item=[]> + Stack<item=[]>]').super(Expr.parse('[Stack<item=[]>]'))
    True

and that although
    not 1.expr.super(2.src)
because

    >>> Expr.parse('[Iterable<item=[]> + Stack<item=[]>]').super(Expr.parse('[Iterable<item=Readable<item=[]>>]'))
    False

if we bind
    1.item from [] to [Readable<item=2.item[]>]
then

    >>> Expr.parse('[Iterable<item=Readable<item=[]>> + Stack<item=Readable<item=[]>>]').super(Expr.parse('[Iterable<item=Readable<item=[]>>]'))
    True

Now the expression for 1 is
    [Iterable<item=[Readable<item=2.item[]>]> + Stack<item=[Readable<item=2.item[]>]>]
This expression involves one of 2's template variables.
"""
}
