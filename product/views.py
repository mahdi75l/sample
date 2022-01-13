from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from product.models import Product, Category
from product.paginations import LargeResultsSetPagination
from product.serializers import ProductSerializer, CategorySerializer, ProductDetailSerializer


class ProductsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.filter(status=True)
    pagination_class = LargeResultsSetPagination
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if not self.kwargs.get('pk'):
            return ProductSerializer
        return ProductDetailSerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        if not self.kwargs.get('pk'):
            return self.queryset.filter(parent__isnull=True)
        return self.queryset

    @action(detail=True, methods=['get'])
    def items(self, request, pk):
        obj = self.get_object()
        paginator = LargeResultsSetPagination()
        queryset = Product.objects.filter(categories__in=obj.get_list_of_childes_id())
        items = paginator.paginate_queryset(queryset=queryset, request=request)
        return paginator.get_paginated_response(ProductSerializer(items, many=True).data)


