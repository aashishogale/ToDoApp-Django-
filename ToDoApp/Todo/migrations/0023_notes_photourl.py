# Generated by Django 2.0.1 on 2018-02-10 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0022_notes_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='photourl',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
