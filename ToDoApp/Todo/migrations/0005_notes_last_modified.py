# Generated by Django 2.0.1 on 2018-02-03 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0004_auto_20180203_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
