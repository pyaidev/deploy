from django.db import models
from django.db.models import SET_NULL
from django.utils import timezone

from config import settings


class Test(models.Model):
    """
    Class for tests
    """
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Description')
    material = models.OneToOneField('education_content.Material', on_delete=models.CASCADE)
    preview = models.ImageField(null=True, blank=True, verbose_name='Preview')
    made_date = models.DateTimeField(default=timezone.now, verbose_name='Creation time')
    last_update = models.DateTimeField(default=timezone.now, verbose_name='Last update teme')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Owner')
    is_published = models.BooleanField(default=False, verbose_name='Publication Status')
    is_published_requested = models.BooleanField(default=False, verbose_name='Publication request status')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Number of Views')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]


class QuestionType(models.Model):
    """
    Class for questions types
    """
    title = models.CharField(max_length=100, verbose_name='Question type')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Question type'
        verbose_name_plural = 'Question types'


class Question(models.Model):
    """
    Class for questions
    """
    text = models.CharField(max_length=500, verbose_name='Question')
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE)
    type = models.ForeignKey('tests.QuestionType', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answers(models.Model):
    """
    Class for answers
    """
    text = models.CharField(max_length=500, verbose_name='Answer')
    question = models.ForeignKey('tests.Question', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False, verbose_name='Is correct answer')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class CompletedTest(models.Model):
    """
    Class for completed tests
    """
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='User')
    passed_time = models.DateTimeField(default=timezone.now, verbose_name='Passed time')

    def __str__(self):
        return f'{self.test} completed'

    class Meta:
        verbose_name = 'Completed test'
        verbose_name_plural = 'Completed tests'


class CompletedQuestion(models.Model):
    """
    Class for completed questions
    """
    completed_test = models.ForeignKey('tests.CompletedTest', on_delete=SET_NULL, null=True, blank=True,
                                       verbose_name='Completed Test')
    question = models.ForeignKey('tests.Question', on_delete=SET_NULL, null=True, blank=True,
                                 verbose_name='Question')
    answer = models.CharField(max_length=500, null=True, blank=True, verbose_name='Users answer')
    is_correct = models.BooleanField(default=False, verbose_name='Was answer correct')

    def __str__(self):
        return f'{self.answer}'

    class Meta:
        verbose_name = 'Completed Question'
        verbose_name_plural = 'Completed Questions'
