# Generated by Django 4.0.3 on 2022-04-09 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_alter_expenses_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="expenses",
            options={"ordering": ["created"]},
        ),
        migrations.AlterOrderWithRespectTo(
            name="expenses",
            order_with_respect_to=None,
        ),
    ]
