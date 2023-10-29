from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Group, Post, Tag, TagPost


class TagSerializer(serializers.ModelSerializer):
    """сериализатор"""
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    """сериализатор"""
    tag = TagSerializer(many=True, required=False)
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(
        source='pub_date', read_only=True
    )
    read_only_fields = ['author']

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'author', 'image',
            'publication_date', 'group', 'tag', 'character_quantity'
        )

    def create(self, validated_data):
        if 'tag' not in self.initial_data:
            return Post.objects.create(**validated_data)

        tag = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)

        for i in tag:
            current_i, status = (
                Tag.objects.get_or_create(**i)
            )
            TagPost.objects.create(
                tag=current_i, post=post
            )
        return post

    def get_character_quantity(self, obj):
        return len(obj.text)


class GroupSerializer(ModelSerializer):
    """сериализатор групп"""
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'description', 'title', 'slug', 'posts')
