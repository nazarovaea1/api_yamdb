# from django.shortcuts import render
# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .models import Category, Genre, Title
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, TitleModifySerializer,
    TitleReadSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('group',)

    def list(self, request):
        queryset = Title.objects.all()
        serializer = TitleReadSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TitleModifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = TitleReadSerializer(title)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = TitleModifySerializer(title, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Title.objects.all()
        title = get_object_or_404(queryset, pk=pk)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
