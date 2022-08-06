from typing import Optional

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

from shared.django import TimeStampMixin


DEFAULT_ROLES = {
    "admin": 1,
    "user": 2,
}


class CustomUserManager(UserManager):
    """Custom user manager."""

    def create_user(self, email, username=None, password=None, **kwargs):
        if not email:
            raise ValueError("Email field is required.")
        if not password:
            raise ValueError("Password field is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        payload: dict = kwargs | {
            "is_superuser": True,
            "is_active": True,
            "is_staff": True,
            "role_id": DEFAULT_ROLES["admin"],
        }
        return self.create_user(email, username, password, **payload)


class Role(TimeStampMixin):
    """User's role. Used for giving permissions."""

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    """This is my castum user"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    phone = models.CharField(max_length=13, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    role = models.ForeignKey(
        "Role",
        null=True,
        default=DEFAULT_ROLES["user"],
        on_delete=models.SET_NULL,
        related_name="users",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updateed_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    class Meta:
        # db_table = "users"
        verbose_name_plural = "Users"
