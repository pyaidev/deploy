# Generated by Django 4.2.5 on 2023-10-12 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Preview'),
        ),
    ]
