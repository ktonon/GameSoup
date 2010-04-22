from django.db import models
from gamesoup.expressions.context import TemplateContext


class SignatureManager(models.Manager):
    def for_signature(self, signature):
        signature = signature.strip()
        qs = self.get_query_set().filter(signature=signature)
        return qs.count() and qs[0] or self.create(signature=signature)


class InterfaceManager(models.Manager):
    
    def for_expr(self, expr):
        return self.get_query_set().filter(name__in=expr.ids)
        
    def any(self):
        try:
            return self.get_query_set().get(is_built_in=False, methods__isnull=True, name='Any')
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist('Please define the Any interface')
    
    def nothing(self):
        try:
            return self.get_query_set().get(is_built_in=True, methods__isnull=True, name='Nothing')
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist('Please define the Nothing interface')


class ParameterManager(models.Manager):
    
    def get_context(self):
        qs = self.get_query_set()
        return TemplateContext([(unicode(p), p.expr) for p in qs.all()])
