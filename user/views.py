from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import Address
from user.serializers import RegisterUserSerializer, AddressSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer_obj = RegisterUserSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        refresh = TokenObtainPairSerializer.get_token(serializer_obj.instance)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class AddressViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


