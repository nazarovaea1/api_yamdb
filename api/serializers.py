from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.FloatField()
    # rating = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Review.objects.all().aggregate(Avg('score')))
    # rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.reviews.exists():
            return obj.reviews.aggregate(rating=Avg('score'))
        return None

    class Meta:
        fields = ('__all__')
        model = Title


class TitleModifySerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        fields = ('__all__')
        model = Title
