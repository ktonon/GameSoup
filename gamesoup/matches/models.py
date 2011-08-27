from django.core.urlresolvers import reverse
from django.db import models
from gamesoup.games.models import *


class Match(models.Model):
    game = models.ForeignKey(Game)
    state = models.TextField(blank=True)

    def __unicode__(self):
        return self.game.name

    class Meta:
        verbose_name_plural = 'Matches'
    
    def play_link(self):
        return '<a href="%s">play</a>' % reverse('matches:play_match', args=[self.id])
    play_link.short_description = 'Play'
    play_link.allow_tags = True
