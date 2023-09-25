# Generated by Django 4.2.5 on 2023-09-24 21:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0002_question_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="order",
            field=models.PositiveIntegerField(
                default=1,
                unique=True,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
