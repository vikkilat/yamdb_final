from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанров."""
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для произведений."""
    list_display = ('pk', 'name', 'year', 'category')
    list_editable = ('name', 'category')
    search_fields = ('name', 'year')
    list_filter = ('name', 'year')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов."""
    list_display = ('pk', 'author', 'title', 'score')
    search_fields = ('author', 'title')
    list_filter = ('author', 'title')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для отзывов."""
    list_display = ('pk', 'author', 'review', 'pub_date')
    search_fields = ('author', 'review')
    list_filter = ('author', 'review', 'pub_date')
    empty_value_display = '-пусто-'
