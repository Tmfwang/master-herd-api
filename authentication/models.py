from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
import uuid
from django.conf import settings

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password, gaards_number=None, bruks_number=None, municipality=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')


        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            gaards_number=gaards_number,
            bruks_number=bruks_number,
            municipality=municipality
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password, gaards_number=None, bruks_number=None, municipality=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')


        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            gaards_number=gaards_number,
            bruks_number=bruks_number,
            municipality=municipality
        )

        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


# User profile models
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    full_name = models.CharField(max_length=150)
    gaards_number = models.CharField(max_length=150, null=True, blank=True) 
    bruks_number = models.CharField(max_length=150, null=True, blank=True)
    municipality = models.CharField(max_length=150, null=True, blank=True)

    is_admin = models.BooleanField(default=False);
   
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    @property
    def is_superuser(self):
        return self.is_admin


   

