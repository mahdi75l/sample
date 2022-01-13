from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('djangoProject.swagger.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('products/', include('product.urls')),
    path('order/', include('order.urls')),
]
