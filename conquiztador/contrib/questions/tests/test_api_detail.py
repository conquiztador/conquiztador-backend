from django.urls import reverse
from rest_framework.test import APITestCase

from conquiztador.mixins import TestMixin


class QuestionDetailTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.question = self.create_question()

        self.create_answer(text="Answer 1")
        self.create_answer(text="Answer 2")
        self.create_answer(text="Answer 3", is_correct=True)

        self.maxDiff = None

    def test_get(self):
        question = self.question
        url = reverse("question-detail", args=[question.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
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

    def test_validate_answer_correct(self):
        url = reverse("question-validate-answer", args=[self.question.pk])

        response = self.client.post(
            url, format="json", data={"uuid": self.question.correct_answer.pk}
        )

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        expected_response = {"is_correct": True}

        self.assertDictEqual(response.json(), expected_response)

    def test_validate_answer_incorrect(self):
        url = reverse("question-validate-answer", args=[self.question.pk])

        incorrect_answer = self.question.answers.filter(is_correct=False).first()

        response = self.client.post(
            url, format="json", data={"uuid": incorrect_answer.pk}
        )

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        expected_response = {"is_correct": False}

        self.assertDictEqual(response.json(), expected_response)
