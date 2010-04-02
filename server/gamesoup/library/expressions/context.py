import UserDict


class TemplateContext(UserDict.UserDict):
    
    def update_with_bindings(self, queryset):
        '''
        Given a queryset of bindings, update this template
        context with any bindings that match parameters.
        '''
        for param_name, expr in self.items():
            try:
                binding = queryset.get(parameter__name=param_name)
                self[param_name] = binding.expression
            except InterfaceTemplateParameterBinding.DoesNotExist:
                pass # It's ok if the type doesn't provide a binding
