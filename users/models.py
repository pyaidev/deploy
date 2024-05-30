from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Remove the username field and replace it with email as the unique identifier
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')  # Email field for authentication
    first_name = models.CharField(max_length=100, verbose_name='First name', null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name='Last name', null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name='Phone Number', null=True, blank=True)
    profile_picture = models.URLField(blank=True, null=True, verbose_name='Profile picture')
    last_activity = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='Last activity')

    # Specify 'email' as the field used for authentication
    USERNAME_FIELD = 'email'

    # No additional fields are required during registration
    REQUIRED_FIELDS = []

    # Use custom User Manager
    objects = CustomUserManager()
