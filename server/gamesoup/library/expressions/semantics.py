'''
For answering questions about how interface expressions relate to each other.
'''


from django.core.urlresolvers import reverse
from gamesoup.library.expressions.syntax import parse_interface_expression


class InterfaceExpression(object):
    '''
    A union of interface expressions.
    '''
    
    def __init__(self, raw_expr):
        '''
        This method is used internally. Use the @classmethod
        InterfaceExpression.parse instead.
        '''
        self._raw_expr = raw_expr
        self._atomics = map(AtomicInterfaceExpression, raw_expr.atomics)

    def __getitem__(self, n):
        '''
        Return the nth AtomicInterfaceExpression that is part
        of this expression.
        '''
        return self._atomics[n]

    def __repr__(self):
        '''
        Convert this expression back into string form.
        '''
        return `self._raw_expr`
    
    def render_with_links(self):
        '''
        Render this expression with links to the interfaces involved.
        '''
        parts = []
        for atom in self._atomics:
            parts.append(atom.render_with_links())
        w = ' & '.join(parts)
        return len(parts) > 1 and '[%s]' % w or w
    
    def _get_interfaces(self):
        return [a.interface for a in self._atomics if not a.is_variable]
    interfaces = property(_get_interfaces)

    def _is_atomic(self):
        '''
        An interface expression is atomic if it only has ONE
        AtomicInterfaceExpression.
        '''
        return len(self._atomics) == 1
    is_atomic = property(_is_atomic)

    def resolve(self, context):
        '''
        Resolve variables in this expression against a context.
        
        The context is a dictionary where keys are variable ids
        and values are interface expressions.
        '''
        atomics = [atom.resolve(context) for atom in self._atomics]
        if len(atomics) > 1:
            return '[%s]' % ' & '.join(atomics)
        else:
            return ' & '.join(atomics)

    @classmethod
    def parse(cls, expression_text):
        '''
        Parse a string form of an interface expression and return
        and instantiated InterfaceExpression.
        '''
        raw_expr = parse_interface_expression(expression_text)
        return cls(raw_expr)


class AtomicInterfaceExpression(object):
    
    def __init__(self, raw_atomic):
        # Intermediate representation
        # an instance of ParsedInterfaceExpression
        self._raw_atomic = raw_atomic
        self._arguments = [(arg.identifier, InterfaceExpression(arg.expression)) for arg in raw_atomic.arguments]
        self._argdict = dict(self._arguments)

    def __repr__(self):
        return `self._raw_atomic`
    
    def render_with_links(self):
        if self.is_variable:
            return self._raw_atomic.identifier
        interface = self.interface
        w = '<a href="%s">%s</a>' % (reverse('admin:library_interface_change', args=[interface.id]), interface.name)
        if self._arguments:
            w += '&lt;%s&gt;' % ','.join(['%s=%s' % (arg[0], arg[1].render_with_links()) for arg in self._arguments])
        return w
    
    def _is_variable(self):
        return self._raw_atomic.is_variable
    is_variable = property(_is_variable)

    def _get_interface(self):
        from gamesoup.library.models import Interface
        if not hasattr(self, '_interface'):
            try:
                self._interface = Interface.objects.get(name=self._raw_atomic.identifier)
            except Interface.DoesNotExist, e:
                raise Interface.DoesNotExist('The interface "%s" refered to in the interface expression "%r" does not exist' % (self._raw_atomic.identifier, self._raw_atomic))
        return self._interface
    interface = property(_get_interface)

    def __getitem__(self, parameter_name):
        return self._argdict[parameter_name]

    def resolve(self, context):
        if self.is_variable:
            id = self._raw_atomic.identifier
            return id in context and `context[id]` or id
        elif self._arguments:
            w = self._raw_atomic.identifier
            args = ['%s=%s' % (arg[0], arg[1].resolve(context)) for arg in self._arguments]
            return '%s<%s>' % (w, ','.join(args))
        else:
            return `self`

    # def tighter_than(self, other):
    #     from gamesoup.library.models import Interface
    #     if self.interface.is_built_in or other.interface.is_built_in:
    #         if other.interface == Interface.objects.any():
    #             return True
    #         else:
    #             return False            
    #     a = self.interface
    #     b = other.interface
    #     for method in other.interface.methods.all():
    #         if self.interface.methods.filter(pk=method.id).count() == 0:
    #             return False
    #     for template_param, other_expr in other._argdict.items():
    #         try:
    #             expr = self._argdict[template_param]
    #         except KeyError:
    #             tp = self.interface.template_parameters.get(name=template_param)
    #             expr = InterfaceExpression(tp.expression_text)
    #         if other_expr.tighter_than(expr) or not (expr.tighter_than(other_expr) or expr.same_as(other_expr)):
    #             return False
    #     return True
    # 
    # def __eq__(self, other): return self.same_as(other)
    # def __lt__(self, other): return self.tighter_than(other)
    # def __gt__(self, other): return other.tighter_than(self)


__test__ = {'doctest': """
>>> from gamesoup.library.expressions.semantics import InterfaceExpression as Expr

>>> any = Expr.parse('Any')
>>> any
Any

>>> Expr.parse('[Any&Nothing]')
[Any & Nothing]

>>> foo = Expr.parse('Foo')

"""}
