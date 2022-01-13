from django.contrib import admin
from django.contrib.auth.models import Group

from user.models import Address

admin.site.register(Address)
admin.site.unregister(Group)

