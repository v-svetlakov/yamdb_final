import uuid

from django.core.cache import cache
from django.core.mail import send_mail

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import AdminPermission
from .serializers import (ConfirmationCodeSerializer, UserEmailSerializer,
                          UserInfoSerializer, UserSerializer)


@api_view(['POST'])
@authentication_classes([])
def send_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        username = serializer.data['username']
        user_is_exist = User.objects.filter(email=email).exists()
        if not user_is_exist:
            cache.set_many({'username': username, 'email': email}, timeout=300)
        confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {confirmation_code}',
            'admin@admin.com',
            [email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
def get_user_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = serializer.data['confirmation_code']
        data = cache.get_many(['username', 'email'])
        username = data['username']
        email = data['email']
        # generate code to check with confirmation code
        code = str(uuid.uuid3(uuid.NAMESPACE_DNS, email))
        if code == confirmation_code:
            token = AccessToken.for_user(username)
            User.objects.create_user(
                username=username,
                email=email)
            return Response({f'token: {token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserInfoSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
