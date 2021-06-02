from django.contrib import admin

from .models import Category, Genre, Title


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
