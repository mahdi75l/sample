from django.contrib import admin

from order.models import Order, SubOrder, Basket

admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(SubOrder)
