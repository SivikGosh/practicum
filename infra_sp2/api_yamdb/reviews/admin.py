from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'author', 'text', 'score', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('author', 'score', 'pub_date')
    empty_value_display = '-пусто-'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'author', 'text', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
