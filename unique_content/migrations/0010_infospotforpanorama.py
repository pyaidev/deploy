# Generated by Django 4.2.5 on 2024-01-30 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unique_content', '0009_figure360view_pano_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoSpotForPanorama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000, verbose_name='Text')),
                ('coord_X', models.FloatField(verbose_name='X coord')),
                ('coord_Y', models.FloatField(verbose_name='Y coord')),
                ('coord_Z', models.FloatField(verbose_name='Z coord')),
                ('panorama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unique_content.figure360view')),
            ],
            options={
                'verbose_name': 'Info spot',
                'verbose_name_plural': 'Info spots',
            },
        ),
    ]
