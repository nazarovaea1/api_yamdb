from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleModifySerializer, TitleReadSerializer,
)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Coalesce(Avg('reviews__score'), None)
        )

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        user = get_object_or_404(User, pk=1)    # TEST
        title = get_object_or_404(Title, pk=title_id)
        # serializer.save(author=self.request.user, title=title)
        serializer.save(author=user, title=title)   # TEST


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        user = get_object_or_404(User, pk=1)    # TEST
        review = get_object_or_404(Review, pk=review_id)
        # serializer.save(author=self.request.user, review=review)
        serializer.save(author=user, review=review)  # TEST
