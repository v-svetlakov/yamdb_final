from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filter import ModelFilter
from .models import Categories, Genre, Title
from .permissions import GeneralPermission
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGeneralSerializer, TitleSlugSerializer)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    serializer_class = CategorySerializer
    permission_classes = [GeneralPermission]
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [GeneralPermission]
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = ModelFilter
    permission_classes = [GeneralPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleGeneralSerializer
        if self.action == 'create':
            return TitleSlugSerializer
        if self.action == 'partial_update':
            return TitleSlugSerializer
        return TitleGeneralSerializer
