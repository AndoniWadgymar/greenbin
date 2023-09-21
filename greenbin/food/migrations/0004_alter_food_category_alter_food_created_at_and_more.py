# Generated by Django 4.1 on 2023-08-20 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("food", "0003_food"),
    ]

    operations = [
        migrations.AlterField(
            model_name="food",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="foods",
                to="food.category",
            ),
        ),
        migrations.AlterField(
            model_name="food",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="food",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="foods",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="food",
            name="weight",
            field=models.IntegerField(),
        ),
    ]