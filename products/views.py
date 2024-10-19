from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Product
from django_filters import rest_framework as filter
from rest_framework import filters

class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (filter.DjangoFilterBackend,filters.SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('name',)
    queryset = Product.objects.all().prefetch_related('images')
    http_method_names=['get']


