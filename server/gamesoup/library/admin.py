from django.contrib import admin
from models import *


class MethodTemplateParameterInline(admin.TabularInline):
    model = MethodTemplateParameter
    fk_name = 'of_method'
    extra = 1
class MethodAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('signature', 'description',)}),
        )
    list_display = ('name', 'used_in_short', 'signature')
    search_fields = ('name', 'returned__interface__name', 'parameters__interface__name', 'used_in__name')
    inlines = (MethodTemplateParameterInline,)
admin.site.register(Method, MethodAdmin)


class MethodTemplateParameterBindingInline(admin.TabularInline):
    model = MethodTemplateParameterBinding
    extra = 3
class InterfaceTemplateParameterInline(admin.TabularInline):
    model = InterfaceTemplateParameter
    fk_name = 'of_interface'
    extra = 1
class InterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_built_in', 'methods')}),
        )
    list_display = ('__unicode__', 'is_built_in', 'doc_link', 'implemented_by_short')
    list_filter = ('is_built_in',)
    search_fields = ('name', 'implemented_by__name', 'methods__name')
    filter_horizontal = ('methods',)
    inlines = (InterfaceTemplateParameterInline, MethodTemplateParameterBindingInline)
    class Media:
        js = (
            'js/lib/prototype.js',
            'js/gamesoup/gamesoup.js',
            'js/gamesoup/library/template-parameter-binding.js',
            )
admin.site.register(Interface, InterfaceAdmin)


class InterfaceTemplateParameterBindingInline(admin.TabularInline):
    model = InterfaceTemplateParameterBinding
    extra = 3
class TypeTemplateParameterInline(admin.TabularInline):
    model = TypeTemplateParameter
    fk_name = 'of_type'
    extra = 1
class TypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', 'visible', 'has_state', 'implements', 'signature', 'code')}),
        )
    list_display = ('name', 'description', 'visible')
    list_filter = ('visible',)
    filter_horizontal = ('implements',)
    search_fields = ('name', 'description', 'implements__name')
    actions = None
    inlines = (TypeTemplateParameterInline, InterfaceTemplateParameterBindingInline)
    class Media:
        js = (
            'js/lib/prototype.js',
            'js/gamesoup/gamesoup.js',
            'js/gamesoup/library/template-parameter-binding.js',
            )
admin.site.register(Type, TypeAdmin)


# class VariableAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {'fields': ('signature',)}),
#         )
#     list_display = ('name', 'interface')
#     search_fields = ('name', 'interface__name')
# admin.site.register(Variable, VariableAdmin)
