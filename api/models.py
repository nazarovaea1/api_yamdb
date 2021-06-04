import textwrap

from django.db import models
from django.db.models.deletion import CASCADE
from pytils.translit import slugify

from api_auth.models import User


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Книги', 'Книги'),
        ('Фильмы', 'Фильмы'),
        ('Музыка', 'Музыка'),
    ]
    name = models.TextField(verbose_name='Категория',
                            help_text='Выберите категорию',
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
        ('Книги', (
            ('Приключения', 'Приключения'),
            ('Фантастика', 'Фантастика'),
            ('Роман', 'Роман'),
        )
        ),
        ('Фильмы', (
            ('Драма', 'Драма'),
            ('Ужасы', 'Ужасы'),
            ('Военный', 'Военный'),
        )
        ),
        ('Музыка', (
            ('Классика', 'Классика'),
            ('Рок', 'Рок'),
            ('Джаз', 'Джаз'),
        )
        ),
    ]

    name = models.TextField(verbose_name='Жанр',
                            help_text='Выберите жанр',
                            choices=GENRE_CHOICES,)
    slug = models.SlugField(max_length=100,
                            unique=True, blank=True,)

    def __str__(self):
        return textwrap.shorten(self.name, width=15)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)





class Reviews(models.Model):
    text = models.TextField(verbose_name='Отзыв',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(verbose_name='Оценка',)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.text[:15]} - {self.author} - {self.pub_date}'


class Comments(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
    )

    def __str__(self):
        return f'{self.text[:15]} - {self.author} - {self.pub_date}'


class Title(models.Model):
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, models.SET_NULL, blank=True,
                                 null=True,
                                 related_name='title')
    genre = models.ManyToManyField(Genre, related_name='title')
    year = models.DecimalField(max_digits=4, decimal_places=0)
    rating = models.ForeignKey(Reviews, models.SET_NULL, blank=True,
                               null=True,
                               related_name='title')

    def __str__(self):
        return textwrap.shorten(self.name, width=15)
