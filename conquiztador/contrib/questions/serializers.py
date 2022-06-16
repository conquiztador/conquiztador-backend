from rest_framework import serializers

from .models import Answer, Category, Question


class AnswerInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "uuid",
            "text",
        )


class AnswerValidationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class CategoryInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "uuid",
            "name",
        )


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerInlineSerializer(many=True, read_only=True)
    categories = CategoryInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            "url",
            "uuid",
            "text",
            "answers",
            "categories",
            "created_at",
            "updated_at",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "url",
            "uuid",
            "name",
            "created_at",
            "updated_at",
        )
