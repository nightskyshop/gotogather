# Generated by Django 2.2 on 2021-12-31 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20211231_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image3',
        ),
    ]