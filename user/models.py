from enum import Enum
from cities_light.models import City
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class RoleEnum(Enum):
    CLIENT = 'C'
    OWNER = 'O'
    STAFF = 'S'


class Role(models.Model):
    ROLES = (
        (RoleEnum.CLIENT.value, 'Client'),
        (RoleEnum.OWNER.value, 'Owner'),
        (RoleEnum.STAFF.value, 'Staff'),
    )
    name = models.CharField(max_length=2, choices=ROLES, unique=True)

    def __str__(self):
        return dict(self.ROLES).get(self.name)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **other_fields):
        if not email:
            raise ValueError('You must provide valid email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **other_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    picture = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    roles = models.ManyToManyField(Role, default='C')
    city = models.ForeignKey(City, null=True, on_delete=models.PROTECT)
    agency = models.ForeignKey('employee.Agency', null=True, blank=True, on_delete=models.PROTECT)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
