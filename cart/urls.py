from rest_framework.routers import DefaultRouter
from .views import CartView,OrderView

router=DefaultRouter()
router.register('cart',CartView,basename='cart')
router.register('order',OrderView,basename='order')
urlpatterns=router.urls