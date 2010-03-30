from django.contrib import admin
from models import *


class GameAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        )
    list_display = ('name', 'get_assembler_link', 'code_link', 'is_satisfied')
    search_fields = ('name', 'object__type__name', 'object__type__implements__name')
admin.site.register(Game, GameAdmin)


class TypeParameterBindingInline(admin.TabularInline):
    model = TypeParameterBinding
    fk_name = 'instance'
    extra = 1
class ObjectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'game', 'type', 'x', 'y', 'width', 'height', 'satisfied', 'per_player')}),
        )
    list_display = ('id', 'name', 'game', 'type', 'x', 'y', 'width', 'height', 'satisfied', 'per_player')
    raw_id_fields = ('game', 'type')
    inlines = [TypeParameterBindingInline]
admin.site.register(Object, ObjectAdmin)
