from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .pagination import CustomPagination
from .permissions import IsSuperuserPermission, IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsSuperuserPermission,
    ]
    lookup_field = 'username'



# class get_confirmation_code(request):