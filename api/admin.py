from django.contrib import admin

from .models import Category, Comments, Genre, Reviews, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'category', 'year')
    search_fields = ('name', 'category', 'genre',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score', 'pub_date')
    search_fields = ('author',)
    list_filter = ('pub_date', 'author',)
    empty_value_display = '-пусто-'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review')
    search_fields = ('author',)
    list_filter = ('pub_date', 'author', 'review')
    empty_value_display = '-пусто-'
