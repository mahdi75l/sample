from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    description = models.TextField()
    count = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('Category', related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_parent = self.parent

    def _get_list_of_childes_id(self, category_id):
        childes = list(Category.objects.filter(parent_id=category_id).values_list('id', flat=True))

        if self.id in childes:
            raise ValidationError('')

        result = childes
        for child_category_id in childes:
            result += self._get_list_of_childes_id(child_category_id)
        return result

    def get_list_of_childes_id(self):
        return list(set(self._get_list_of_childes_id(self.id)))

    def __str__(self):
        return self.name

    def clean(self):
        if self.id and self.id == self.parent:
            raise ValidationError('You can not select this category as parent')

        if self.old_parent != self.parent:
            print('hi')

        super(Category, self).clean()
