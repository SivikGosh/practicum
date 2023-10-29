from django.contrib import admin
from titles.models import Category, Genre, GenreTitle, Title


class CategoryAdmin(admin.ModelAdmin):
    """модель категории произведения"""
    list_display = ('pk', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    """модель жанра произведения"""
    list_display = ('pk', 'name', 'slug')


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle


class TitleAdmin(admin.ModelAdmin):
    """модель произведения"""
    inlines = [GenreTitleInline]
    list_display = ('pk', 'name', 'year', 'description', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
