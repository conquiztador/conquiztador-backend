from rest_framework import serializers

from .models import Answer, Question


class AnswerInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "uuid",
            "text",
        )

class AnswerValidationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            "url",
            "uuid",
            "text",
            "answers",
            "created_at",
            "updated_at",
        )
