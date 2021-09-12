import random

from django.db import models


class QuestionManager(models.Manager):
    def get_random(self):
        index = random.randint(0, self.count() - 1)

        return self.all()[index]
