from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    security_answer1 = models.CharField(max_length=100)
    security_answer2 = models.CharField(max_length=100)
    security_answer3 = models.CharField(max_length=100)

    # Додаємо унікальні related_name для уникнення конфліктів
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions_set',
        related_query_name='user'
    )

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'