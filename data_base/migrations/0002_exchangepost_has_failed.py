# Generated by Django 5.0.4 on 2024-06-19 00:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchangepost",
            name="has_failed",
            field=models.BooleanField(default=False),
        ),
    ]
