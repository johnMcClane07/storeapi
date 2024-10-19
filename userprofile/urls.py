from django.contrib import admin
from django.urls import path, include
from .views import FavouriteView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('favourites', FavouriteView, basename='favourites')

urlpatterns = [ 

    path('', include(router.urls)),

    

]