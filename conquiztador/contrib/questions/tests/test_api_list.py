from django.urls import reverse
from rest_framework.test import APITestCase

from conquiztador.mixins import TestMixin

from ..models import Question


class QuestionListTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.question = self.create_question()

        self.create_answer(text="Answer 1")
        self.create_answer(text="Answer 2")
        self.create_answer(text="Answer 3", is_correct=True)

        self.maxDiff = None

    def test_get(self):
        url = reverse("question-list")
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        questions = Question.objects.all()

        expected_response = {
            "count": len(questions),
            "next": None,
            "previous": None,
            "results": [
                {
                    "url": response.wsgi_request.build_absolute_uri(
                        reverse("question-detail", args=[question.pk])
                    ),
                    "uuid": str(question.pk),
                    "text": question.text,
                    "answers": [
                        {
                            "uuid": str(answer.pk),
                            "text": answer.text,
                        }
                        for answer in question.answers.all()
                    ],
                    "updated_at": question.updated_at.astimezone().isoformat(),
                    "created_at": question.created_at.astimezone().isoformat(),
                }
                for question in questions
            ],
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_get_random(self):
        url = reverse("question-get-random")

        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        question = Question.objects.first()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("question-detail", args=[question.pk])
            ),
            "uuid": str(question.pk),
            "text": question.text,
            "answers": [
                {
                    "uuid": str(answer.pk),
                    "text": answer.text,
                }
                for answer in question.answers.all()
            ],
            "updated_at": question.updated_at.astimezone().isoformat(),
            "created_at": question.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)
