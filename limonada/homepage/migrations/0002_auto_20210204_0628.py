# Generated by Django 2.2.13 on 2021-02-04 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='volume',
            field=models.CharField(blank=True, default='', max_length=30),
            preserve_default=False,
        ),
    ]
