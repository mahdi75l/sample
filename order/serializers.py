import random
import string

from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import Basket, Order, SubOrder
from product.serializers import ProductSerializer
from user.serializers import AddressSerializer


class CreateBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('id', 'product', 'count', 'modified_at')
        extra_kwargs = {
            'user': {'write_only': True},
            'modified_at': {'read_only': True}
        }

    def get_fields(self):
        fields = super(CreateBasketSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields

    def validate_product(self, attrs):
        if not (attrs or attrs.status):
            raise ValidationError('this product is not available')
        return attrs

    def validate_count(self, attrs):
        if attrs < 1:
            raise ValidationError('count must be >1')
        return attrs

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['obj'] = Basket.objects.filter(user=attrs['user'], product=attrs['product']).first()
        old_count = attrs['obj'].count if attrs['obj'] else 0
        if attrs['product'].count + old_count < attrs['count']:
            raise ValidationError('The number of orders should not exceed the inventory')

        return attrs
    
    def create(self, validated_data):
        old_order = validated_data.pop('obj')
        validated_data['product'].count -= validated_data['count']
        if old_order:
            validated_data['product'].count += old_order.count
            old_order.count = validated_data['count']
            validated_data['product'].save()
            old_order.save()
            return old_order
        validated_data['product'].save()
        return super(CreateBasketSerializer, self).create(validated_data)


class BasketSerializer(CreateBasketSerializer):
    product = ProductSerializer()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'address', 'description')

    def validate_address(self, attrs):
        user = self.context['request'].user
        if user.id != attrs.user_id:
            raise ValidationError('you cant pick this address')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['total_price'] = Basket.objects.filter(
            user=validated_data['user']
        ).aggregate(total_price=Sum('product__price')).get('total_price')

        if not validated_data['total_price']:
            raise ValidationError('basket is empty')
        validated_data['transaction_number'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

        order = super(PaymentSerializer, self).create(validated_data)
        return order


class CheckPaymentSerializer(serializers.Serializer):
    transaction_number = serializers.CharField(max_length=64, required=True)
    status = serializers.BooleanField(default=False)

    def validate(self, attrs):
        order = Order.objects.filter(transaction_number=attrs['transaction_number']).first()
        if not order:
            raise ValidationError('not found')
        attrs['order'] = order
        return attrs

    def create(self, validated_data):
        order = validated_data.pop('order')
        order.status = validated_data.get('status', False)
        order.save()

        if order.status:
            bulk_list = []
            for item in Basket.objects.filter(user=order.user).prefetch_related('product'):
                bulk_list.append(
                    SubOrder(order=order, product=item.product, price=item.product.price, count=item.count))
            SubOrder.objects.bulk_create(bulk_list)
            Basket.objects.filter(user=order.user).delete()

        return order


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ('id', 'address', 'description', 'total_price', 'transaction_number', 'status')


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ('id', 'address', 'description', 'total_price', 'transaction_number', 'status', 'items')

    def get_items(self, obj):
        sub_order = obj.sub_orders.all()
        return SubOrderSerializer(instance=sub_order, many=True).data


class SubOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SubOrder
        fields = ('id', 'product', 'price', 'count')



