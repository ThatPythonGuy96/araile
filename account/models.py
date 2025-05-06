from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
import os
from django.core.validators import FileExtensionValidator

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

def get_profile_image(instance, filename):
    upload_to = '{}/{}'.format('account', instance.pk)
    ext = filename.split('.')[-1]
    filename = '{}_{}.{}'.format('Profile', instance.pk, ext)
    return os.path.join(upload_to, filename)

class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, max_length=10, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=get_profile_image, blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    date_joined = models.DateTimeField(auto_now_add=True)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = AccountManager()

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.email