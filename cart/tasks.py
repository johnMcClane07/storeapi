from celery import shared_task
from django.core.cache import cache
from django.db.models import Sum
from rest_framework.response import Response
from .models import Cart, CartProduct, Order, OrderProduct
from django.db.models import F
from django.db import transaction

@shared_task
def create_order(cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return {'error': 'Cart not found'}

    cache_key = f'total_price_{cart.user.id}'
    total_price = cache.get(cache_key)

    if total_price is None:
        total_price_data = cart.cartproduct_set.aggregate(
            total_price=Sum(F('product__final_price') * F('quantity'))
        )
        total_price = total_price_data['total_price'] or 0  
        cache.set(cache_key, total_price)

    try:
        with transaction.atomic():
            order = Order.objects.create(user=cart.user, total_price=total_price)

            order_products = [
                OrderProduct(
                    order=order,
                    product=cart_product.product,
                    quantity=cart_product.quantity
                )
                for cart_product in cart.cartproduct_set.all()
            ]

            OrderProduct.objects.bulk_create(order_products)
            cart.delete()

        return {'id': order.id}  

    except Exception as e:
        return {'error': 'Failed to create order'}
