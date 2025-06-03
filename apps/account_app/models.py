from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.core.validators import EmailValidator, MinLengthValidator


class CustomUser(AbstractUser):
    # Override the 'username' field to remove it
    username = None

    email = models.EmailField(verbose_name='email address', null=True, blank=True,  validators=[EmailValidator])
    phone = models.CharField(max_length=11, unique=True, validators=[MinLengthValidator(11)])

    USERNAME_FIELD = "phone"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-date_joined',)

    def __str__(self):
        return self.get_full_name()
