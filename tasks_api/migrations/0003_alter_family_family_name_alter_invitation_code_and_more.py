# Generated by Django 5.0.6 on 2024-07-16 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_api', '0002_task_duration_in_seconds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='family_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='possibletask',
            name='possible_task_name',
            field=models.CharField(max_length=13),
        ),
    ]
