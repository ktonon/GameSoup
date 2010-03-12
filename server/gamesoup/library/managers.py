from django.db import models
from gamesoup.library.choices import *


class SignatureManager(models.Manager):
    def for_signature(self, signature):
        signature = signature.strip()
        qs = self.get_query_set().filter(signature=signature)
        return qs.count() and qs[0] or self.create(signature=signature)
