from django.contrib import admin
from models import *


class MatchAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('game', 'state')}),
        )
    list_display = ('game', 'play_link')
admin.site.register(Match, MatchAdmin)
