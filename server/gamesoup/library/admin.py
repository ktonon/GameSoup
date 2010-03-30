from django.contrib import admin
from models import *


class MethodAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('interface', 'signature', 'description',)}),
        )
    list_display = ('name', 'signature', 'interface')
    list_filter = ('interface',)
    search_fields = ('name', 'returned__interface__name', 'parameters__interface__name', 'interface__name')
admin.site.register(Method, MethodAdmin)


class MethodInline(admin.StackedInline):
    model = Method
    fields = ('signature', 'description')
    extra = 1
class InterfaceTemplateParameterInline(admin.TabularInline):
    model = InterfaceTemplateParameter
    fk_name = 'of_interface'
    extra = 1
class InterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_built_in')}),
        )
    list_display = ('__unicode__', 'is_built_in', 'doc_link', 'implemented_by_short')
    list_filter = ('is_built_in',)
    search_fields = ('name', 'implemented_by__name', 'methods__name')
    inlines = (InterfaceTemplateParameterInline, MethodInline)
    class Media:
        js = (
            'js/lib/prototype.js',
            'js/gamesoup/gamesoup.js',
            'js/gamesoup/library/template-parameter-binding.js',
            )
admin.site.register(Interface, InterfaceAdmin)


class TypeParameterInline(admin.TabularInline):
    model = TypeParameter
    extra = 3
class InterfaceTemplateParameterBindingInline(admin.TabularInline):
    model = InterfaceTemplateParameterBinding
    fields = ('parameter', 'bound_to')
    extra = 3
class TypeTemplateParameterInline(admin.TabularInline):
    model = TypeTemplateParameter
    fk_name = 'of_type'
    extra = 1
class TypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', ('visible', 'has_state'), 'implements')}),
        )
    list_display = ('name', 'description', 'visible')
    list_filter = ('visible',)
    filter_horizontal = ('implements',)
    search_fields = ('name', 'description', 'implements__name')
    actions = None
    inlines = (TypeTemplateParameterInline, TypeParameterInline, InterfaceTemplateParameterBindingInline)
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
