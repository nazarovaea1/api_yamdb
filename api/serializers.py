from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')
        model = Title


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

    def validate_score(self, value):
        if value < 1 and value > 10:
            raise serializers.ValidationError('ERROR: score is fail')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
