from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import TitleFilter
from .models import Category, Genre, Title
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, TitleModifySerializer,
    TitleReadSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == ('create' or 'partial_update'):
            return TitleModifySerializer
        return TitleReadSerializer

    def perform_create(self, serializer):
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def perform_create(self, serializer):
        serializer.save()
