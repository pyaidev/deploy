# Generated by Django 4.2.5 on 2024-02-03 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unique_content', '0015_infospotforpanorama_figure_3d_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='infospotforpanorama',
            name='youtube_for_iframe',
            field=models.URLField(blank=True, null=True, verbose_name='Iframe video link'),
        ),
    ]