from django.contrib import admin

from tests.models import Test, QuestionType, Question, Answers, CompletedTest, CompletedQuestion


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('text',)


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_filter = ('text',)


@admin.register(CompletedTest)
class CompletedTestAdmin(admin.ModelAdmin):
    list_filter = ('test',)


@admin.register(CompletedQuestion)
class CompletedQuestionAdmin(admin.ModelAdmin):
    list_filter = ('completed_test',)
