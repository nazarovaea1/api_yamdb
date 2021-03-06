import textwrap

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from pytils.translit import slugify

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.TextField(verbose_name='Категория',
                            help_text='Выберите категорию',)
    slug = models.SlugField(max_length=100,
                            unique=True, blank=True,)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return textwrap.shorten(self.name, width=15)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.TextField(verbose_name='Жанр',
                            help_text='Выберите жанр',)
    slug = models.SlugField(max_length=100,
                            unique=True, blank=True,)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return textwrap.shorten(self.name, width=15)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Title(models.Model):
    name = models.TextField(max_length=200)
    description = models.TextField(blank=True,
                                   null=True,)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='title',)
    genre = models.ManyToManyField(Genre, related_name='title', blank=True,)
    year = models.IntegerField(blank=True, null=True,
                               validators=[validate_year])

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return textwrap.shorten(self.name, width=15)


class Review(models.Model):
    text = models.TextField(verbose_name='Отзыв',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        choices=[(i, i) for i in range(1, 11)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведения')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.text[:15]} - {self.author} - {self.pub_date}'


class Comment(models.Model):
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
        Review,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='Отзывы',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.text[:15]} - {self.author} - {self.pub_date}'
