from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, 'Аутентифицированный'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        blank=True,
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.IntegerField(
        'Код подтверждения',
        null=True,
    )

    class Meta:
        ordering = ['-id']

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
