# Generated by Django 2.0.1 on 2018-02-06 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0014_notes_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='color',
            field=models.CharField(default='#ffffff', max_length=2000),
        ),
    ]
