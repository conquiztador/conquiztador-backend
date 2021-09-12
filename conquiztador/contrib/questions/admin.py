from django.contrib import admin

from .models import Answer, Question


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ("author", "created_at", "updated_at")
    list_display = ("text", "author", "created_at", "updated_at")
    list_per_page = 15
    date_hierarchy = "created_at"
    search_fields = ("text", "author")
    inlines = [
        AnswerInline,
    ]
