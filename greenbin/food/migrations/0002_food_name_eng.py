# Generated by Django 3.2.20 on 2023-09-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='name_eng',
            field=models.CharField(default='name', max_length=255),
        ),
    ]