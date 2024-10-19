from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductView

routers=DefaultRouter()
routers.register('products',ProductView)


urlpatterns = [

    path('',include(routers.urls))
]