# Generated by Django 2.0.1 on 2018-02-01 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0002_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]
