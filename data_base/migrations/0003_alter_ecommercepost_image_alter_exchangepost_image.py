# Generated by Django 5.0.4 on 2024-05-09 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_base', '0002_rename_tittle_ecommercepost_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecommercepost',
            name='image',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='exchangepost',
            name='image',
            field=models.BinaryField(),
        ),
    ]
