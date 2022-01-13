from django.contrib.auth.models import User
from django.db import models

from product.models import Product
from user.models import Address


class Basket(models.Model):
    user = models.ForeignKey(User, related_name='basket_user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='basket_user', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, related_name='order_address', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    transaction_number = models.CharField(max_length=25)
    status = models.BooleanField(default=False)


class SubOrder(models.Model):
    order = models.ForeignKey(Order, related_name='sub_orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='sub_orders', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()



