# Generated by Django 2.2 on 2021-11-25 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_uplesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='upclass',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='posts.Class'),
        ),
    ]