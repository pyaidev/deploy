# Generated by Django 4.2.5 on 2023-10-06 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education_content', '0010_alter_chapter_last_update_alter_material_last_update'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Question type')),
            ],
            options={
                'verbose_name': 'Question type',
                'verbose_name_plural': 'Question types',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('made_date', models.DateField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('last_update', models.DateField(default=django.utils.timezone.now, verbose_name='Last update date')),
                ('is_published', models.BooleanField(default=False, verbose_name='Publication Status')),
                ('is_published_requested', models.BooleanField(default=False, verbose_name='Publication request status')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Number of Views')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_content.material')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Tests',
                'permissions': [('set_published', 'Can publish posts')],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Question')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.test')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.questiontype')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='CompletedTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passed_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Passed time')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.test')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Completed test',
                'verbose_name_plural': 'Completed tests',
            },
        ),
        migrations.CreateModel(
            name='CompletedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=500, null=True, verbose_name='Users answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Was answer correct')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tests.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is correct answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
