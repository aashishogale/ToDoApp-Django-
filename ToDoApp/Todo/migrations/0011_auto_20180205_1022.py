# Generated by Django 2.0.1 on 2018-02-05 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0010_auto_20180205_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='models'),
        ),
    ]