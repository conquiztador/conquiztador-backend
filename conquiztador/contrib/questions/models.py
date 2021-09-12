import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from conquiztador.models import TimestampedModel

from . import managers

UserModel = get_user_model()


class Question(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    text = models.CharField(_("Text"), max_length=254)
    author = models.ForeignKey(
        UserModel, related_name="questions", on_delete=models.CASCADE
    )

    objects = managers.QuestionManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("questions:detail", kwargs={"pk": self.pk})

    @property
    def correct_answer(self):
        return self.answers.filter(is_correct=True).first()


class Answer(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    text = models.CharField(_("Text"), max_length=254)
    author = models.ForeignKey(
        UserModel, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name="answers",
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
        blank=True,
        null=True,
    )
    is_correct = models.BooleanField(_("Is correct"), default=False)

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("questions:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.is_correct and self.question.correct_answer:
            raise ValueError(_("A question can only have a single correct answer"))

        return super().save(*args, **kwargs)
