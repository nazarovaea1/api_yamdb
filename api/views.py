# from django.shortcuts import render
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Category, Genre, Title
from .permissions import IsAdminUserOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()
