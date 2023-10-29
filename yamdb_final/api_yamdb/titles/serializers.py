from datetime import date

from django.db.models import Avg
from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = models.Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = models.Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=models.Genre.objects
    )

    def validate_year(self, value):
        if value < date.today().year:
            return value
        raise serializers.ValidationError('Проверьте год!')

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = models.Title

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = models.Title.objects.create(**validated_data)
        for genre in genres:
            models.GenreTitle.objects.create(genre=genre, title=title)
        return title

    def get_rating(self, obj):
        rating = None
        avg_rating = obj.reviews.aggregate(Avg('score'))
        if avg_rating['score__avg']:
            rating = int(avg_rating['score__avg'])
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_name = models.Category.objects.get(
            slug=representation["category"]).name
        representation["category"] = {
            'name': category_name,
            'slug': representation["category"]
        }

        genre_list = []
        for genre in representation["genre"]:
            genre_name = models.Genre.objects.get(slug=genre).name
            genre_list.append(
                {
                    'name': genre_name,
                    'slug': genre
                }
            )
        representation["genre"] = genre_list
        return representation
