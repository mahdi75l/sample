from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from user.views import RegisterUserAPIView, AddressViewSet

router = routers.SimpleRouter()
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
]

urlpatterns += router.urls
