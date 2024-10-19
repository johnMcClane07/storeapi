from rest_framework import serializers
from .models import Favourite
from products.models import Product, ProductImages


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']

class ProductInFavouriteSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images']

class FavouriteSerializer(serializers.ModelSerializer):
    product = ProductInFavouriteSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Favourite
        fields = ['id', 'product', 'user']