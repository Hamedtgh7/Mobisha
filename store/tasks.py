from __future__ import absolute_import, unicode_literals
from django.core.serializers.json import DjangoJSONEncoder
from celery import shared_task
from decimal import Decimal
from .models import PriceChange, Seller, Product
import redis
import json


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@shared_task
def create_price_change(product_id, new_price, seller_id):

    with redis.Redis('localhost', port=6379) as redis_cache:
        cache_key = f'origin_product_{product_id},seller_{seller_id}'
        data = json.loads(redis_cache.get(cache_key))
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.get(id=product_id)
        PriceChange.objects.create(
            product=product,
            old_price=data['price'],
            new_price=new_price,
            seller=seller
        )

        json_data = json.dumps({'price': new_price}, cls=DecimalEncoder)
        redis_cache.set(cache_key, value=json_data)
