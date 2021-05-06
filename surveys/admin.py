from django.contrib import admin
from .models import Surveys, Questions, AnswerChoices


class AnswerChoicesInline(admin.TabularInline):
    model = AnswerChoices


class QuestionsAdmin(admin.ModelAdmin):
    inlines = [AnswerChoicesInline]


admin.site.register(Surveys)
admin.site.register(Questions, QuestionsAdmin)