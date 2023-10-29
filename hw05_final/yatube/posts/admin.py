""" модели приложения posts в админке """

from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    """ модель поста """
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ['text']
    list_filter = ['pub_date']
    list_editable = ['group']
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """ модель группы """
    list_display = ('pk', 'title', 'slug', 'description')


class CommentAdmin(admin.ModelAdmin):
    """ модель комментария """
    list_display = ('post', 'author', 'text', 'created')
    search_fields = ['author']
    list_filter = ['created']


class FollowAdmin(admin.ModelAdmin):
    """ модель подписки """
    list_display = ('author', 'user')
    search_fields = ['author']
    list_filter = ['author']


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
