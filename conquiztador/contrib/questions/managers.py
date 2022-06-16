import random

from django.db import models


class QuestionManager(models.Manager):
    def get_random(self, category=None):
        if category:
            queryset = self.filter(categories__in=category)
        else:
            queryset = self.all()

        index = random.randint(0, queryset.count() - 1)

        return queryset[index]
