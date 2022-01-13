from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=64)
    address = models.TextField()


