# Generated by Django 2.0.1 on 2018-02-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0009_auto_20180205_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
