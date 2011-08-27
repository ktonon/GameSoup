from django.contrib import admin
from models import *


class GameAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        )
    list_display = ('name', 'get_assembler_link', 'code_link', 'updated_at')
    search_fields = ('name', 'object__type__name', 'object__type__implements__name')
admin.site.register(Game, GameAdmin)


class ObjectTemplateParameterInline(admin.TabularInline):
    model = ObjectTemplateParameter
    extra = 0
class TypeTemplateParameterBindingInline(admin.TabularInline):
    model = TypeTemplateParameterBinding
    fields = ('parameter', 'expression_text')
    extra = 0
class ObjectTemplateParameterBindingInline(admin.TabularInline):
    model = ObjectTemplateParameterBinding
    fields = ('parameter', 'expression_text')
    extra = 1
class ObjectParameterInline(admin.TabularInline):
    model = ObjectParameter
    extra = 0
class ObjectParameterBindingInline(admin.TabularInline):
    model = ObjectParameterBinding
    fk_name = 'instance'
    extra = 0
class ObjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', ('x', 'y'), ('width', 'height'), 'per_player')}),
        )
    list_display = ('id', 'name', 'game', 'type', 'x', 'y', 'width', 'height', 'per_player')
    raw_id_fields = ('game', 'type')
    inlines = (ObjectTemplateParameterInline, TypeTemplateParameterBindingInline, ObjectTemplateParameterBindingInline, ObjectParameterInline, ObjectParameterBindingInline)
admin.site.register(Object, ObjectAdmin)
