from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from apps.address.models import Location


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email, is_staff=True, is_superuser=True, is_active=True, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    is_verified = models.BooleanField(default=False)
    username = None
    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="address"
    )
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="user_address"
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.first_name
