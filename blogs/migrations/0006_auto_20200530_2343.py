# Generated by Django 3.0.6 on 2020-05-30 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20200530_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(default='1'),
        ),
    ]
