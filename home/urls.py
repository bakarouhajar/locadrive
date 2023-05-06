from django.urls import path, re_path
from . import views

app_name = 'home'

urlpatterns = [
    path("", views.cars, name="index"),
    path("cars", views.cars, name="cars"),
    path("client_rentals/", views.client_rentals, name='client_rentals'),
    path("car_details/<int:car_id>/", views.car_details, name='car_details'),
    path('rent_car/<int:car_id>/', views.rent_car, name='rent_car'),

]