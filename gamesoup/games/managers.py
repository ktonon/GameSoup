from django.db import models


class GameObjectManager(models.Manager):
    
    def bindable_to(self, other_obj, type_param):
        '''
        Return objects which are bindable to other_obj.param(type_param)
        '''
        qs = self.get_query_set().filter(game=other_obj.game)
        return qs.filter()
