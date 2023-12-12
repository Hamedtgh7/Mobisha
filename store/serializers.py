from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Seller, Product, PriceChange


class LoginSellerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = get_object_or_404(Seller, username=username)

        if user.password != password:
            return serializers.ValidationError('Invalid password')

        return data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'price']


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['price']


class PriceChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceChange
        fields = ['product', 'old_price', 'new_price', 'updated_at', 'seller']
