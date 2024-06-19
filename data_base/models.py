from django.db import models
from django.utils import timezone
from datetime import timedelta


class Workers(models.Model):
    name = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=20)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    birth_day = models.DateField(blank=True)
    password = models.CharField(max_length=8)


class Affiliate(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    birth_day = models.DateField(blank=True)
    password = models.CharField(max_length=8)
    points = models.IntegerField(default=0)
    login_attemps = models.IntegerField(default=0)
    rejected_posts = models.IntegerField(default=0)


class Reputation(models.Model):
    reputation = models.FloatField(default=3.0)
    affiliate = models.ForeignKey(
        Affiliate, on_delete=models.CASCADE, related_name="affiliate"
    )
    to_do = models.BooleanField(default=False)
    comes_from_affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comes_from_affiliate",
    )


class Tokens(models.Model):
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    token = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateTimeField()


class Branches(models.Model):
    worker = models.ForeignKey(Workers, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    latitude = models.FloatField()
    altitude = models.FloatField()


class AccountBlock(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    is_permanent = models.BooleanField(default=False)
    end_timestamp = models.DateTimeField(null=True)


class Workers_AccountBlock(models.Model):
    worker = models.ForeignKey(Workers, on_delete=models.CASCADE)
    account_block = models.ForeignKey(AccountBlock, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


class ProductCategory(models.Model):
    name = models.CharField(max_length=20)


class Products(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


class Affiliate_Need_Product(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class ExchangePost(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=20)
    image = models.BinaryField(null=True, blank=True)
    description = models.TextField(max_length=300)
    timestamp = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    has_failed = models.BooleanField(default=False)

class EcommercePost(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    image = models.BinaryField(null=True, blank=True)
    description = models.TextField(max_length=300)
    point_cost = models.IntegerField()
    stock = models.IntegerField()


class Affiliate_EcommercePost(models.Model):
    ecommerce_post = models.ForeignKey(EcommercePost, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    total_cost_in_points = models.IntegerField()


class ExchangeSolicitude(models.Model):
    exchange_post_for_id = models.ForeignKey(
        ExchangePost, on_delete=models.CASCADE, related_name="exchange_post_for_id"
    )
    in_exchange_post_id = models.ForeignKey(
        ExchangePost, on_delete=models.CASCADE, related_name="in_exchange_post_id"
    )
    affiliate_id = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    denied = models.BooleanField(default=False)
    timestamp = models.DateTimeField()


class Exchange(models.Model):
    """
    Represents an exchange between two affiliates. The `Exchange` model stores information about the exchange, including the exchange solicitude, the two affiliates involved, and the codes associated with the exchange.

    Attributes:
        exchange_solicitude (ExchangeSolicitude): The exchange solicitude that this exchange is associated with.
        affiliate_1 (Affiliate): The first affiliate involved in the exchange (requester).
        affiliate_2 (Affiliate): The second affiliate involved in the exchange (reciever).
        code1 (str): A 5-character code associated with the exchange.
        code2 (str): Another 5-character code associated with the exchange.
        timestamp (datetime): The timestamp of when the exchange occurred phisically.
    """

    exchange_solicitude = models.ForeignKey(
        ExchangeSolicitude, on_delete=models.CASCADE
    )
    affiliate_1 = models.ForeignKey(
        Affiliate, on_delete=models.CASCADE, related_name="affiliate_1"
    )
    affiliate_2 = models.ForeignKey(
        Affiliate, on_delete=models.CASCADE, related_name="affiliate_2"
    )
    code1 = models.CharField(max_length=5, unique=True, null=True)
    code2 = models.CharField(max_length=5, unique=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    branch = models.ForeignKey(
        Branches, on_delete=models.SET_NULL, null=True, blank=True
    )
    exchange_date = models.DateField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)


class Donation(models.Model):
    amount = models.FloatField()
    timestamp = models.DateTimeField()
