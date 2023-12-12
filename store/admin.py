from django.contrib import admin
from .models import Seller, Product


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'last_update']
