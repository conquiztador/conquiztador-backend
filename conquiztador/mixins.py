from django.contrib.auth import get_user_model

from conquiztador.contrib.questions.models import Answer, Question

UserModel = get_user_model()


class TestMixin:
    def create_user(
        self, email="john.doe@example.com", password="password", **extra_fields
    ):
        return UserModel.objects.create_user(
            email=email, password=password, **extra_fields
        )

    def create_question(self, text="Question text", author=None):
        return Question.objects.create(
            text=text,
            author=author or self.user,
        )

    def create_answer(
        self, text="Answer text", is_correct=False, question=None, author=None
    ):
        return Answer.objects.create(
            text=text,
            is_correct=is_correct,
            question=question or self.question,
            author=author or self.user,
        )
