from django.contrib import admin
from models import *


class InterfaceTemplateParameterInline(admin.TabularInline):
    model = InterfaceTemplateParameter
    fk_name = 'of_interface'
    extra = 1
class InterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_built_in', 'signature')}),
        )
    list_display = ('__unicode__', 'is_built_in', 'doc_link', 'implemented_by_short')
    list_filter = ('is_built_in',)
    search_fields = ('name', 'implemented_by__name', 'methods__name')
    inlines = (InterfaceTemplateParameterInline,)
admin.site.register(Interface, InterfaceAdmin)


class TypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description', 'visible', 'has_state', 'implements', 'signature', 'code')}),
        )
    list_display = ('name', 'description', 'visible')
    list_filter = ('visible',)
    filter_horizontal = ('implements',)
    search_fields = ('name', 'description', 'implements__name')
    actions = None
admin.site.register(Type, TypeAdmin)


class MethodAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('description',)}),
        )
    list_display = ('name', 'used_in_short', 'signature')
    search_fields = ('name', 'returned__interface__name', 'parameters__interface__name', 'used_in__name')
admin.site.register(Method, MethodAdmin)


# class VariableAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {'fields': ('signature',)}),
#         )
#     list_display = ('name', 'interface')
#     search_fields = ('name', 'interface__name')
# admin.site.register(Variable, VariableAdmin)
