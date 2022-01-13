from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Address


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.save()

        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'title', 'address')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(AddressSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(AddressSerializer, self).update(instance, validated_data)
