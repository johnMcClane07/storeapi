from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FavouriteSerializer
from .models import Favourite
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import requests
from rest_framework.decorators import action


class FavouriteView(ModelViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete', 'get']
    
    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user).select_related('product').prefetch_related('product__images')
    
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if Favourite.objects.filter(user=user, product=kwargs['pk']).exists():
            Favourite.objects.filter(user=user, product=kwargs['pk']).delete()
        return super().destroy(request, *args, **kwargs)    
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        product=request.data.get('product')
        if not Favourite.objects.filter(user=user, product_id=product).exists():
            Favourite.objects.get_or_create(user=user, product_id=product)
        else:
            return Response({"error": "Product is already in favourites"}, status=400)
        return Response({"message": "Product added to favourites"}, status=201)