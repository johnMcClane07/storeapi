from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CartSerializer,  OrderSerializer
from .models import Cart, CartProduct, Order
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from .tasks import create_order
from celery.result import AsyncResult


class CartView(ModelViewSet):
    serializer_class = CartSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related('cartproduct_set')  

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        cache_key = f'total_price_{request.user.id}'
        total_price = cache.get(cache_key)

        if total_price is None:
            try:
                total_price = queryset.aggregate(
                    total_price=Sum('cartproduct__product__final_price') * Sum('cartproduct__quantity')
                )['total_price']
                cache.set(cache_key, total_price, 60)
            except Exception:
                return Response({"error": "Error calculating total price"}, status=500)

        response = super().list(request, *args, **kwargs)
        response.data = {'cart': response.data[0], 'total_price': total_price}
        return response

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity'))
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=Product.objects.get(id=product_id),
            defaults={'quantity': quantity}
        )
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        cache.delete(f'total_price_{user.id}')
        return Response({'message': 'Product added to cart'})
    
    @action(methods=['delete'], detail=False, url_path='remove-product')
    def remove_product(self, request):
        product = request.data.get('product')
        cart_product = CartProduct.objects.filter(cart=Cart.objects.filter(user=request.user).first(), product=product).first()

        if cart_product.quantity > 1:
            cart_product.quantity -= 1
            cart_product.save()
            cache.delete(f'total_price_{request.user.id}')
            return Response({'message': 'Product removed from cart'})
        
        elif cart_product.quantity == 1:
            cart_product.delete()
            cache.delete(f'total_price_{request.user.id}')
            return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response({'message': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['delete'], detail=False, url_path='clear-cart')
    def clear_cart(self, request):
        user = request.user
        cart=Cart.objects.filter(user=user).first()
        CartProduct.objects.filter(cart=cart).delete()
        cache.delete(f'total_price_{request.user.id}')
        return Response({'message': 'Корзина очищена'})
    
    @action(methods=['post'], detail=False, url_path='create-order')
    def make_order(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'message': 'Корзина пуста'})
        create_order.delay(cart_id=cart.id)

        return Response({'message': 'Заказ создан'})
    
class OrderView(ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get', 'delete']
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('orderproduct_set')
    

    

    




