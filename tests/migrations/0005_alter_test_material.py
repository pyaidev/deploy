# Generated by Django 4.2.5 on 2023-10-13 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education_content', '0010_alter_chapter_last_update_alter_material_last_update'),
        ('tests', '0004_alter_completedquestion_options_alter_test_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='material',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='education_content.material'),
        ),
    ]
