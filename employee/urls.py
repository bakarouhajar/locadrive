from django.urls import path

from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.index, name='index'),
    # path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('add-car/', views.add_car, name='add_car'),
    path('cars/', views.cars, name='cars'),
    path('update-car/<int:car_id>/', views.update_car, name='update_car'),
    path('delete-car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('detail-car/<int:car_id>/', views.detail_car, name='detail_car'),
    path('update_rental/', views.update_rental, name='rentals'),
    path('rentals/', views.rentals, name='rentals'),
    path('rental-income/', views.rental_income, name='rental_income'),
    path('owner/profile/', views.owner_profile, name='owner_profile'),
    path('detail_client/<int:client_id>', views.detail_client, name='detail_client'),
    path('agency/', views.agency_view, name='agency'),

]
