import random

from django.db import models


class QuestionManager(models.Manager):
    def get_random(self, category=None):
        queryset = self.all()

        if category is not None:
            queryset = queryset.filter(categories=category)

        if not queryset.exists():
            raise models.ObjectDoesNotExist("No question matches the given category.")

        return queryset.order_by("?").first()
