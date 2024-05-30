from django import forms

from tests.models import Test, CompletedTest, Question, Answers
from users.forms import StyleFormMixin


class TestForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'material', 'preview', 'owner', 'is_published', 'is_published_requested',)


class TestUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'preview', 'owner', 'is_published', 'is_published_requested',)


class QuestionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'type', 'test',)


class AnswersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Answers
        fields = ('text', 'question', 'is_correct',)


class CompletedTestForm(forms.ModelForm):
    class Meta:
        model = CompletedTest
        fields = ('test', 'user', 'passed_time',)
