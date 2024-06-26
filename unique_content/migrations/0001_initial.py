# Generated by Django 4.2.5 on 2023-11-16 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FigureThinSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Rock title')),
                ('description', models.CharField(max_length=500, verbose_name='Description')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Preview')),
                ('file', models.FileField(upload_to='', verbose_name='File')),
                ('made_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation time')),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last update time')),
                ('is_ppl', models.BooleanField(default=True, verbose_name='Is Parallel Nicols')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Thin Section',
                'verbose_name_plural': 'Thin Sections',
            },
        ),
        migrations.CreateModel(
            name='FigureFromP3din',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.CharField(max_length=500, verbose_name='Description')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Preview')),
                ('link', models.CharField(max_length=300, verbose_name='Link to p3d.in')),
                ('made_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation time')),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last update time')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': '3D figure',
                'verbose_name_plural': '3D figures',
            },
        ),
    ]
