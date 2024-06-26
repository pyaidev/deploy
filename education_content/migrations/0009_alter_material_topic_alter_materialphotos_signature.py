# Generated by Django 4.2.5 on 2023-10-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0008_alter_chapter_options_alter_material_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='topic',
            field=models.CharField(max_length=100, verbose_name='Topic'),
        ),
        migrations.AlterField(
            model_name='materialphotos',
            name='signature',
            field=models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='Signature'),
        ),
    ]
