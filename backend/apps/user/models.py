from ..core.models import BaseModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(
        db_index=True,
        unique=True,
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)

    USERNAME_FIELD = "email"

    reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_expiration = models.DateTimeField(blank=True, null=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_jwt_tokens(self):
        refresh = RefreshToken.for_user(self)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}
