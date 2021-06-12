from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USER_ROLES = (USER, MODERATOR, ADMIN)


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
        default=USER
    )
    email = models.EmailField(_('email address'))

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.email