# Generated by Django 2.0.1 on 2018-02-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0003_auto_20180201_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='isArchived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notes',
            name='isPinned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notes',
            name='isTrashed',
            field=models.BooleanField(default=False),
        ),
    ]
