# Generated by Django 5.0.4 on 2024-05-31 13:38

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
                ('points', models.IntegerField(default=0)),
                ('login_attemps', models.IntegerField(default=0)),
                ('rejected_posts', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('altitude', models.FloatField()),
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
                ('image', models.BinaryField(blank=True, null=True)),
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
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
            ],
        ),
        migrations.CreateModel(
            name='Affiliate_EcommercePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField()),
                ('total_cost_in_points', models.IntegerField()),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('ecommerce_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.ecommercepost')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('image', models.BinaryField(blank=True, null=True)),
                ('description', models.TextField(max_length=300)),
                ('timestamp', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_base.productcategory')),
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
                ('code1', models.CharField(max_length=5, null=True, unique=True)),
                ('code2', models.CharField(max_length=5, null=True, unique=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('exchange_date', models.DateField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('affiliate_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_1', to='data_base.affiliate')),
                ('affiliate_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_2', to='data_base.affiliate')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_base.branches')),
                ('exchange_solicitude', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.exchangesolicitude')),
            ],
        ),
        migrations.AddField(
            model_name='ecommercepost',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.productcategory'),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Affiliate_Need_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.products')),
            ],
        ),
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reputation', models.FloatField(default=3.0)),
                ('to_do', models.BooleanField(default=False)),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate', to='data_base.affiliate')),
                ('comes_from_affiliate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comes_from_affiliate', to='data_base.affiliate')),
            ],
        ),
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=16, unique=True)),
                ('expiration_date', models.DateTimeField()),
                ('affiliate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.affiliate')),
            ],
        ),
        migrations.AddField(
            model_name='branches',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.workers'),
        ),
        migrations.CreateModel(
            name='Workers_AccountBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('account_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.accountblock')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_base.workers')),
            ],
        ),
    ]
