from django.contrib import admin
from .models import Rental, Car, Agency, CarModel, CarBrand

admin.site.register(Rental)
admin.site.register(Car)
admin.site.register(Agency)
admin.site.register(CarModel)
admin.site.register(CarBrand)
