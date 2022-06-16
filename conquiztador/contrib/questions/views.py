from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers


class QuestionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.QuestionSerializer
    http_method_names = ("get",)
    queryset = models.Question.objects.all()

    def get_serializer_class(self):
        if self.action == "validate_answer":
            return serializers.AnswerValidationSerializer

        return super().get_serializer_class()

    @action(detail=False, methods=("get",), url_path="random")
    def get_random(self, request, pk=None):
        question = models.Question.objects.get_random()

        serializer = serializers.QuestionSerializer(
            question, context={"request": request}, many=False
        )

        return Response(serializer.data)

    @action(detail=True, methods=("post",), url_path="validate-answer")
    def validate_answer(self, request, pk=None):
        question = self.get_object()
        serializer = serializers.AnswerValidationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        is_correct = question.correct_answer.uuid == serializer.validated_data.get(
            "uuid"
        )

        return Response({"is_correct": is_correct})


class CategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.CategorySerializer
    http_method_names = ("get",)
    queryset = models.Category.objects.all()

    @action(detail=True, methods=("get",))
    def questions(self, request, pk=None):
        category = self.get_object()
        questions = category.questions.all()

        serializer = serializers.QuestionSerializer(
            questions, context={"request": request}, many=True
        )

        return Response(serializer.data)

    @action(detail=True, methods=("get",), url_path="questions/random")
    def random_question(self, request, pk=None):
        category = self.get_object()
        question = category.questions.get_random()

        serializer = serializers.QuestionSerializer(
            question, context={"request": request}, many=False
        )

        return Response(serializer.data)
