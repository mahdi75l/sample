from rest_framework import routers

from order.views import BasketAPIView, OrderAPIView

router = routers.SimpleRouter()
router.register(r'basket', BasketAPIView)
router.register(r'', OrderAPIView)


urlpatterns = [
]

urlpatterns += router.urls

