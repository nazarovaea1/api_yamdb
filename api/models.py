import textwrap

from django.db import models
from pytils.translit import slugify


class Category(models.Model):
    BOOKS = 'BOOK'
    MOVIES = 'MOV'
    MUSIC = 'MSC'
    CATEGORY_CHOICES = [
        (BOOKS, 'Книги'),
        (MOVIES, 'Фильмы'),
        (MUSIC, 'Музыка'),
    ]
    name = models.TextField(verbose_name="Категория",
                            help_text="Выберите категорию",
                            choices=CATEGORY_CHOICES,)
    slug = models.SlugField(max_length=100,
                            unique=True, blank=True,)

    def __str__(self):
        return textwrap.shorten(self.name, width=15)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Genre(models.Model):
    GENRE_CHOICES = [
        ('book_genres', (
            ('adventures', 'Приключения'),
            ('fantasy', 'Фантастика'),
            ('novel', 'Роман'),
        )
        ),
        ('movie_genres', (
            ('drama', 'Драма'),
            ('horror', 'Ужасы'),
            ('adventures', 'Приключения'),
        )
        ),
        ('music_genres', (
            ('classic', 'Классика'),
            ('rock', 'Рок'),
            ('jazz', 'Джаз'),
        )
        ),
    ]

    name = models.TextField(verbose_name="Жанр",
                            help_text="Выберите жанр",
                            choices=GENRE_CHOICES,)
    slug = models.SlugField(max_length=100,
                            unique=True, blank=True,)

    def __str__(self):
        return textwrap.shorten(self.name, width=15)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Title(models.Model):
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, models.SET_NULL, blank=True,
                                 null=True,
                                 related_name="title")
    genre = models.ManyToManyField(Genre, related_name="title")
    year = models.DecimalField(max_digits=4, decimal_places=0)
    # rating = models.ForeignKey(Rating, models.SET_NULL, blank=True,
    #                            null=True,
    #                            related_name="title")

    def __str__(self):
        return textwrap.shorten(self.name, self.description, width=15)
