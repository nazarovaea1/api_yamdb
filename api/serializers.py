from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_text(self, value):
        method = self.context.get('request').method
        author = self.context.get('request').user
        title_id = self.context['view'].kwargs['title_id']

        review = Review.objects.filter(
            author=author, title_id=title_id).exists()

        if method == 'POST' and review:
            raise serializers.ValidationError('Вы уже оставляли отзыв')

        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.FloatField()

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
