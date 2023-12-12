from django.core.validators import MinValueValidator
from django.db import models


class Seller(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name='products')


class PriceChange(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='changes')
    old_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    new_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
