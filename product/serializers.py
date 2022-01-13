from rest_framework import serializers

from product.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'count', 'price', 'categories')

    def get_categories(self, obj):
        return obj.categories.all().values_list('id', 'name')


class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'count', 'price', 'categories', 'description')


class CategorySerializer(serializers.ModelSerializer):
    childes = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'childes')

    def get_childes(self, obj):
        result = ""
        childes = Category.objects.filter(parent=obj)
        if childes:
            result = []
            for child in childes:
                result.append(CategorySerializer(instance=child).data)
        return result
