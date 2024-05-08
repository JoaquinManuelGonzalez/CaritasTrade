from django.db import models

class Workers(models.Model):
    name = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=20)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    birth_day = models.DateField(blank=True)
    password = models.CharField(max_length=8)

class Reputation(models.Model) : 
    reputation = models.FloatField(default=3.0)

class Affiliate (models.Model): 
    reputation_id = models.ForeignKey(Reputation, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    birth_day = models.DateField()
    password = models.CharField(max_length=8)

class Branches (models.Model): 
    worker_id = models.ForeignKey(Workers, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    latitude = models.FloatField()
    altitude = models.FloatField()

class AccountBlock(models.Model): 
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    is_permanent = models.BooleanField(default=False)
    end_timestamp = models.DateTimeField(null=True)

class Workers_AccountBlock (models.Model): 
    worker_id = models.ForeignKey(Workers, on_delete=models.CASCADE)
    account_block_id = models.ForeignKey(AccountBlock, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class ProductCategory(models.Model) : 
    name = name = models.CharField(max_length=20)

class Products(models.Model) : 
    product_category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

class Affiliate_Product(models.Model) : 
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)

class ExchangePost(models.Model) : 
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product_category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    image = models.ImageField()
    description = models.TextField(max_length=300)
    timestamp = models.DateTimeField()
    is_active = models.BooleanField(default=False)

class EcommercePost(models.Model) :
    product_category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    image = models.ImageField()
    description = models.TextField(max_length=300)
    point_cost = models.IntegerField()
    stock = models.IntegerField()

class Affiliate_EcommercePost(models.Model) : 
    ecommerce_post_id = models.ForeignKey(EcommercePost, on_delete=models.CASCADE)
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    total_cost_in_points = models.IntegerField()

class ExchangeSolicitude(models.Model) : 
    exchange_post_for_id = models.ForeignKey(ExchangePost, on_delete=models.CASCADE, related_name="exchange_post_for_id")
    in_exchange_post_id = models.ForeignKey(ExchangePost, on_delete=models.CASCADE, related_name="in_exchange_post_id")
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    denied = models.BooleanField(default=False)
    timestamp = models.DateTimeField()

class Exchange(models.Model) :
    exchange_solicitude_id = models.ForeignKey(ExchangeSolicitude, on_delete=models.CASCADE)
    affiliate_1_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name="affiliate_1_id")
    affiliate_2_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name="affiliate_2_id")
    code1 = models.CharField(max_length=5)
    code2 = models.CharField(max_length=5)
    timestamp = models.DateTimeField()

class Donation(models.Model) :
    amount = models.FloatField()
    timestamp = models.DateTimeField()