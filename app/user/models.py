"""
Define Database Models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from .validators import phone_validator


class UserManager(BaseUserManager):
    """
    Manager class to manage user objects of a custom user model.
    """

    def create_user(self, phone, name, password, email=None):
        """
        Create a new user with phone number, name and password.
        """
        if not phone:
            raise ValueError("User must have an email address.")
        elif not name:
            raise ValueError("User must have a name.")
        elif not password:
            raise ValueError("User must have a password.")
        if email:
            email = self.normalize_email(email)
        user = self.model(phone=phone, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password, email=None):
        """
        Create a new superuser.
        """

        user = self.create_user(phone, name, password, email=email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Define a custom user model.
    """

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25, unique=True, validators=[phone_validator])
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = [
        "name",
    ]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """
        Define how User object is displayed in the django admin panel.
        """
        return f"{self.name} - {self.phone}"
