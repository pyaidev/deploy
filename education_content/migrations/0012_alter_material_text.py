# Generated by Django 4.2.5 on 2023-11-04 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0011_material_is_test_exist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
    ]
