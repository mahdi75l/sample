from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from order.models import Basket, Order
from order.serializers import PaymentSerializer, CheckPaymentSerializer, BasketSerializer, \
    OrderSerializer, OrderDetailsSerializer, CreateBasketSerializer


class BasketAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Basket.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBasketSerializer
        return BasketSerializer

    def list(self, request, *args, **kwargs):
        data = {
            'item': self.get_serializer(instance=self.get_queryset(), many=True).data,
            'count_item': len(self.get_serializer(instance=self.get_queryset(), many=True).data),
            'total_price': 0
        }

        for obj in data['item']:
            data['total_price'] += (obj.get('product').get('price') * obj.get('count'))
        return Response(data)

    @action(detail=False, methods=['Post'])
    def payment(self, request):
        serialized_data = PaymentSerializer(data=request.data, context={'request':request})
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['Post'])
    def check_payment(self, request):
        serialized_data = CheckPaymentSerializer(data=request.data, context={'request': request})
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(status=status.HTTP_201_CREATED)


class OrderAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(methods=['get'], detail=True)
    def details(self, request, pk):
        serialized_obj = OrderDetailsSerializer(instance=self.get_object())
        return Response(serialized_obj.data)
