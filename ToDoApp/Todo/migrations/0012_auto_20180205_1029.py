# Generated by Django 2.0.1 on 2018-02-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo', '0011_auto_20180205_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]