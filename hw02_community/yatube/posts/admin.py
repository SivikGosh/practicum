"""Модели в админке"""

from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    """Модель поста в админке"""

    list_display = ('pk',
                    'text',
                    'pub_date',
                    'author',
                    'group')

    search_fields = ['text']
    list_filter = ['pub_date']
    list_editable = ['group']

    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """Модель поста в админке"""

    list_display = ('pk',
                    'title',
                    'slug',
                    'description')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
