# Generated by Django 2.2.28 on 2025-04-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lipids', '0002_auto_20210204_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lipid',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
