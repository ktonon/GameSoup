from django.contrib import admin
from models import *


class GameAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        )
    list_display = ('name', 'is_satisfied')
admin.site.register(Game, GameAdmin)


# class BindingInline(admin.TabularInline):
#     model = Binding
#     fk_name = 'instance'
#     extra = 0
# class ObjectAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {'fields': ('game', 'type', 'x', 'y', 'width', 'height', 'satisfied', 'per_player')}),
#         )
#     list_display = ('id', 'game', 'type', 'x', 'y', 'width', 'height', 'satisfied', 'per_player')
#     inlines = [BindingInline]
# admin.site.register(Object, ObjectAdmin)
