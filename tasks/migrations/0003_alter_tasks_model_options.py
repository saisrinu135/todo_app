# Generated by Django 4.2.7 on 2023-11-20 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_tasks_model_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasks_model',
            options={'ordering': ['completed']},
        ),
    ]
