# Generated by Django 4.2.5 on 2023-11-22 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0016_rename_figure_materialphotos_preview_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialphotos',
            name='preview',
        ),
        migrations.AlterField(
            model_name='materialphotos',
            name='signature',
            field=models.CharField(default='Signature not entered', max_length=300, verbose_name='Signature'),
        ),
    ]
