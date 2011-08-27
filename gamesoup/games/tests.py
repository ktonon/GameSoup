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

    def test_dynamic_object_typing_with_int_pusher(self):
        int_stack = self.ipush.get_parameter('stack')
        # Before
        self.assertEquals(`self.list.final_expr`, '[Stack<item=[%d.item]>]' % self.list.id)
        self.assertEquals(`int_stack.final_expr`, '[Stack<item=Integer!>]')

        # Do binding...
        self.ipush.bind_parameter('stack', self.list)

        # After
        # The type of list should be dynamically changed so that
        # it is super to string_stack
        self.assertTrue(self.list.final_expr > int_stack.final_expr)
    
    def test_dynamic_object_typing_with_string_pusher(self):
        string_stack = self.spush.get_parameter('stack')
        # Before
        self.assertEquals(`self.list.expr`, '[Stack<item=[]>]')
        self.assertEquals(`string_stack.expr`, '[Stack<item=String!>]')
        
        # Do binding...
        self.spush.bind_parameter('stack', self.list)

        # After
        # The type of list should be dynamically changed so that
        # it is super to string_stack
        self.assertTrue(self.list.final_expr > string_stack.final_expr)

    def test_object_parameter_resolvent_for_type(self):
        int_stack = self.ipush.get_parameter('stack')
        list_type = Type.objects.get(name='List')
        resolvent = int_stack.resolvent_for(list_type)
        self.assertEquals(`resolvent`, '@List.item : Integer!')

    def test_search_for_stack_for_int_pusher(self):
        int_stack = self.ipush.get_parameter('stack')
        candidates = int_stack.candidate_types
        self.assertEquals(len(candidates), 1)
