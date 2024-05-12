# Generated by Django 5.0.4 on 2024-05-10 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_base', '0002_exchangepost_is_rejected'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=16, unique=True)),
                ('expiration_date', models.DateTimeField()),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
            ],
        ),
    ]
