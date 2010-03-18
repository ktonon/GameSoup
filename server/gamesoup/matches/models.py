from django.db import models
from gamesoup.games.models import *


class Match(models.Model):
    game = models.ForeignKey(Game)
    state = models.TextField(blank=True)

    def __unicode__(self):
        return self.game.name

    class Meta:
        verbose_name_plural = 'Matches'