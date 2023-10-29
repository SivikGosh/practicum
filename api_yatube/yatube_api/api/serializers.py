from posts.models import Comment, Group, Post
from rest_framework.serializers import ModelSerializer, SlugRelatedField


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group

        # не могу определиться какие поля оставлять, а какие нет,
        # поэтому указываю '__all__' :)
        #
        # насколько это хороший тон?
        # или лучше изначально внести все поля в список поимённо,
        # а в дальнейшем, если появятся ещё,
        # добавлять в этот же список при необходимости?
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
