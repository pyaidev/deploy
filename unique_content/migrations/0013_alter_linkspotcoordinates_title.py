# Generated by Django 4.2.5 on 2024-01-31 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unique_content', '0012_alter_infospotforpanorama_title_linkspotcoordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkspotcoordinates',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Title'),
        ),
    ]
