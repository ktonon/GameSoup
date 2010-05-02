from django.test import TestCase
from gamesoup.library.models import *
from gamesoup.games.models import *


class GameTest(TestCase):

    fixtures = ['test-data', 'test-library', 'test-games']
    
    def setUp(self):
        self.game = Game.objects.get(name='Foggle')
        self.list = self.game.object_set.get(type__name='List')
        self.spush = self.game.object_set.get(type__name='StringPusher')
        self.ipush = self.game.object_set.get(type__name='IntegerPusher')
    
    def test_dynamic_object_typing(self):
        self.assertEquals(`self.spush.flat_expr`, '[]')
        self.assertEquals(`self.ipush.flat_expr`, '[]')

        self.assertEquals(`self.list.flat_expr`, '[Stack<item=[%d.item]>]' % self.list.id)
        self.assertEquals(`self.list.expr`, '[Stack<item=[]>]')
        self.assertEquals(`self.list.final_expr`, '[Stack<item=[%d.item]>]' % self.list.id)

        self.spush.bind('stack', self.list)
