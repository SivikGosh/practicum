import base64

from django.core.files.base import ContentFile
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class GroupSerializer(serializers.ModelSerializer):
    """сериализатор групп"""
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class Base64ImageField(serializers.ImageField):
    """декодер поля 'image' поста"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """сериализатор постов"""
    author = serializers.StringRelatedField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = (
            'id', 'author', 'text', 'pub_date', 'image', 'group', 'comments'
        )
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """сериализатор комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """сериализатор подписок"""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True, default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("Подписка на себя запрещена!")
        return value

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=['user', 'following']
            )
        ]
