# Generated by Django 5.0.4 on 2024-05-09 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchangepost',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]