# Generated by Django 4.2.5 on 2023-09-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0004_chapter_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Publication Status'),
        ),
    ]
