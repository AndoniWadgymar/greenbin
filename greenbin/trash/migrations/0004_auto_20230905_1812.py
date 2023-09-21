# Generated by Django 3.2.20 on 2023-09-06 00:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trash', '0003_trash_on_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='trash',
            name='user_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trash',
            name='user_size',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(500.0)]),
        ),
    ]
