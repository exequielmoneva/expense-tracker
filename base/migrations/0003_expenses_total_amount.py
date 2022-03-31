# Generated by Django 4.0.3 on 2022-03-31 12:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_rename_expense_expenses"),
    ]

    operations = [
        migrations.AddField(
            model_name="expenses",
            name="total_amount",
            field=models.FloatField(
                default=0.01,
                validators=[django.core.validators.MinValueValidator(0.01)],
            ),
        ),
    ]
