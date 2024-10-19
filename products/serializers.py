from rest_framework import serializers
from .models import Product, ProductImages, Category

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImages
        fields=['image']
class ProductSerializer(serializers.ModelSerializer):
    images=ProductImagesSerializer(many=True)
    class Meta:
        model=Product
        fields= '__all__'
