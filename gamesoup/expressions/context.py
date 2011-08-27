import UserDict


class TemplateContext(UserDict.UserDict):
    
    def update_with_bindings(self, queryset):
        '''
        Given a queryset of bindings, update this template
        context with any bindings that match parameters.
        '''
        from gamesoup.library.models import InterfaceTemplateParameterBinding
        for param_name, expr in self.items():
            try:
                binding = queryset.get(parameter__name=param_name)
                self[param_name] = binding.expr
            except InterfaceTemplateParameterBinding.DoesNotExist:
                pass # It's ok if the type doesn't provide a binding

    def __str__(self):
        return str(unicode(self))
        
    def __unicode__(self):
        '''
        >>> from gamesoup.expressions.syntax import Expr
        >>> e = Expr.parse('[]')
        >>> c = TemplateContext({
        ...     'I.b': e,
        ...     'I.a': e,
        ...     'I.c': e,
        ... })
        >>> print "%s" % c
        a=[],b=[],c=[]
        '''
        return ','.join([
            '%s=%r' % (k.split('.')[1], v)
            for k, v in sorted(self.items())
            ])

    def __repr__(self):
        '''
        >>> from gamesoup.expressions.syntax import Expr
        >>> e = Expr.parse('[]')
        >>> c = TemplateContext({
        ...     'I.b': e,
        ...     'I.a': e,
        ...     'I.c': e,
        ... })
        >>> c
        I.a : []
        I.b : []
        I.c : []
        >>> TemplateContext({})
        <BLANKLINE>
        '''
        # Items sorted by keys
        return '\n'.join([
            '%s : %r' % (k, v)
            for k, v in sorted(self.items())
            ])