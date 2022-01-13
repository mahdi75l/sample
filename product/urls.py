from django.urls import path
from rest_framework import routers

from product.views import ProductsViewSet, CategoryViewSet

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet)
router.register(r'item', ProductsViewSet)

urlpatterns = [
    # path('category/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('category/products', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
