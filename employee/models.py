from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from cities_light.models import City

from user.models import CustomUser


class Agency(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + ' ' + self.city.name


class CarBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=150, unique=True)
    car_model_price = models.FloatField()
    car_brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Car(models.Model):
    GEARBOXES = (
        ('AT', 'Automatic'),
        ('MT', 'Manual'),
    )

    FUELS = (
        ('G', 'Gasoline'),
        ('D', 'Diesel'),
        ('H', 'Hybrid'),
        ('E', 'Electric'),
    )
    registration_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    year = models.IntegerField()
    doors = models.PositiveSmallIntegerField()
    seats = models.PositiveSmallIntegerField()
    ac = models.BooleanField()
    gearbox = models.CharField(max_length=2, choices=GEARBOXES)
    fuel = models.CharField(max_length=1, choices=FUELS)
    picture = models.ImageField(upload_to='cars/', default='cars/default.png')
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.car_model)


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(CustomUser, related_name='client', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    paid = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.client.username) + str(self.car.car_model)

    def calculate_cost(self):
        days = (self.end_date - self.start_date).days + 1
        return days * self.rental_price

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date.')