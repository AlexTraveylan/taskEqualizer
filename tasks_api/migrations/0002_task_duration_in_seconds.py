# Generated by Django 5.0.6 on 2024-06-19 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='duration_in_seconds',
            field=models.IntegerField(default=0),
        ),
    ]