# Generated by Django 4.2.5 on 2023-11-16 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0014_alter_chapter_last_update_alter_chapter_made_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialphotos',
            name='figure_3d',
        ),
        migrations.AlterField(
            model_name='materialphotos',
            name='figure',
            field=models.ImageField(default=None, upload_to='', verbose_name='Figure'),
            preserve_default=False,
        ),
    ]
