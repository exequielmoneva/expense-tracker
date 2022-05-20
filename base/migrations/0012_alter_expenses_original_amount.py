# Generated by Django 4.0.3 on 2022-05-20 10:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0011_remove_expenses_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expenses",
            name="original_amount",
            field=models.FloatField(
                validators=[django.core.validators.MinValueValidator(0.01)]
            ),
        ),
    ]
