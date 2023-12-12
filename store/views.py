from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from decimal import Decimal
from .serializers import LoginSellerSerializer, ProductSerializer, UpdateProductSerializer, PriceChangeSerializer
from .models import Product, Seller, PriceChange
from .tasks import create_price_change
import json
import redis
import jwt


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSellerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        id = Seller.objects.get(username=username).id
        payload = {
            'username': username,
            'id': id
        }
        token = jwt.encode(
            payload=payload, key=settings.JWT_KEY, algorithm='HS256'
        )
        return Response(token)


class ProductViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return UpdateProductSerializer
        else:
            return ProductSerializer

    def get_queryset(self):
        username = self.request.allow
        seller = Seller.objects.get(username=username)
        return Product.objects.filter(seller=seller)

    def perform_create(self, serializer):
        username = self.request.allow
        seller = Seller.objects.get(username=username)
        serializer.validated_data['seller'] = seller
        serializer.save()
        with redis.Redis('localhost', port=6379) as redis_cache:
            cache_key = f'origin_product_{serializer.instance.id},seller_{seller.id}'
            json_srializer = json.dumps(
                {'price': serializer.validated_data['price']}, cls=DecimalEncoder)
            redis_cache.set(cache_key, value=json_srializer)

    def perform_update(self, serializer):
        username = self.request.allow
        seller = Seller.objects.get(username=username)
        serializer.validated_data['seller'] = seller
        serializer.save()
        create_price_change.delay(
            serializer.instance.id, serializer.validated_data['price'], seller.id)


class PriceChangeViewSet(ListModelMixin, GenericViewSet):
    queryset = PriceChange.objects.all()
    serializer_class = PriceChangeSerializer
