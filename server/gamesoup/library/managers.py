from django.db import models


class SignatureManager(models.Manager):
    def for_signature(self, signature):
        signature = signature.strip()
        qs = self.get_query_set().filter(signature=signature)
        return qs.count() and qs[0] or self.create(signature=signature)


class InterfaceManager(models.Manager):
    
    def any(self):
        try:
            return self.get_query_set().get(is_built_in=False, signature='', name='Any')
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist('Please define the Any interface')
    
    def nothing(self):
        try:
            return self.get_query_set().get(is_built_in=True, signature='', name='Nothing')
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist('Please define the Nothing interface')
