# Generated by Django 4.0.3 on 2022-04-09 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_alter_expenses_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="expenses",
            old_name="total_amount",
            new_name="original_amount",
        ),
    ]
