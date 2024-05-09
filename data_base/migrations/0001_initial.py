# Generated by Django 5.0.4 on 2024-05-09 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=10)),
                ('birth_day', models.DateField(blank=True)),
                ('password', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EcommercePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('image', models.BinaryField()),
                ('description', models.TextField(max_length=300)),
                ('point_cost', models.IntegerField()),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reputation', models.FloatField(default=3.0)),
            ],
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=10)),
                ('birth_day', models.DateField(blank=True)),
                ('password', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='AccountBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_permanent', models.BooleanField(default=False)),
                ('end_timestamp', models.DateTimeField(null=True)),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
            ],
        ),
        migrations.CreateModel(
            name='Affiliate_EcommercePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField()),
                ('total_cost_in_points', models.IntegerField()),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('ecommerce_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.ecommercepost')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('image', models.BinaryField()),
                ('description', models.TextField(max_length=300)),
                ('timestamp', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('product_category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeSolicitude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denied', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField()),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('exchange_post_for_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_post_for_id', to='data_base.exchangepost')),
                ('in_exchange_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_exchange_post_id', to='data_base.exchangepost')),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code1', models.CharField(max_length=5)),
                ('code2', models.CharField(max_length=5)),
                ('timestamp', models.DateTimeField()),
                ('affiliate_1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_1_id', to='data_base.affiliate')),
                ('affiliate_2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_2_id', to='data_base.affiliate')),
                ('exchange_solicitude_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.exchangesolicitude')),
            ],
        ),
        migrations.AddField(
            model_name='ecommercepost',
            name='product_category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.productcategory'),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('product_category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Affiliate_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.products')),
            ],
        ),
        migrations.AddField(
            model_name='affiliate',
            name='reputation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.reputation'),
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('altitude', models.FloatField()),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.workers')),
            ],
        ),
        migrations.CreateModel(
            name='Workers_AccountBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('account_block_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.accountblock')),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.workers')),
            ],
        ),
    ]
