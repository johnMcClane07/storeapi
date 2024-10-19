from rest_framework import serializers
from .models import Cart,CartProduct,Order,OrderProduct



class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartProduct
        fields=['id', 'product', 'quantity']

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderProduct
        fields='__all__'
    
class CartSerializer(serializers.ModelSerializer):
    cartproduct_set=CartProductSerializer(many=True,read_only=True)
    total_price=serializers.IntegerField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Cart
        fields=["id","total_price","cartproduct_set","user_id"]

class OrderSerializer(serializers.ModelSerializer):
    orderproduct_set=OrderProductSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields='__all__'
    
