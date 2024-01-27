from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractUser,
    AbstractBaseUser,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        """Create and save a new user"""
        if not email:
            raise ValueError("Email adresse is compulsory!")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(default="", max_length=50, blank=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
