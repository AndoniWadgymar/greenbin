# Generated by Django 3.2.20 on 2023-09-25 22:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20230925_0855'),
        ('trash', '0002_alter_trash_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trash',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Duración'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Término'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='foods',
            field=models.ManyToManyField(related_name='food', to='food.Food', verbose_name='Alimentos'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='on_process',
            field=models.BooleanField(default=False, verbose_name='En Proceso'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='processed_size',
            field=models.FloatField(blank=True, null=True, verbose_name='Tamaño Procesado'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='size',
            field=models.CharField(choices=[('S', 'Chico (100g-200g)'), ('M', 'Mediano (200g-350g)'), ('L', 'Grande (350g-500g)')], default='M', max_length=2, verbose_name='Tamaño'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Inicio'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='start_date_formated',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Fecha Formato'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='user_duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Duración Específica'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='user_size',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(500.0)], verbose_name='Tamaño Específico'),
        ),
    ]
