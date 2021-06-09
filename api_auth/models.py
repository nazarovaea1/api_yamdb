from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_yamdb.settings import USER_ROLES


class User(AbstractUser):
    """ A custom user model to customize it if the need arises """

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='description'
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='user'
    )
    email = models.EmailField(_('email address'))

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.email
