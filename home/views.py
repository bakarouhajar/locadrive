from datetime import datetime

from _decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from employee.models import Car, Rental
from user.views import get_custom_user_roles


# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def cars(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        # Validate the dates
        today = datetime.today().strftime('%Y-%m-%d')
        if from_date < today:
            messages.error(request, 'From date cannot be earlier than today.')
            return redirect('home:cars')
        elif to_date < from_date:
            messages.error(request, 'To date cannot be earlier than from date.')
            return redirect('home:cars')

        cars = Car.objects.exclude(
            Q(rental__start_date__lte=to_date, rental__end_date__gte=from_date) &
            Q(rental__paid=True)
        )
        context = {'cars': cars}
        return render(request, 'home/index.html', context)
    else:
        context = {}
        return render(request, 'home/index.html', context)


@login_required
def rent_car(request, car_id):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, 'Login first.')
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if user_roles['is_owner']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('employee:index')
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        # check if the rental dates are valid (i.e. not already rented)
        if Rental.objects.filter(car=car, start_date__lte=to_date, end_date__gte=from_date, paid=True).exists():
            messages.error(request, 'The car is not available for the selected dates.')
            return redirect('home:index')

        rental_days = (to_date - from_date).days + 1
        car_model_price = car.car_model.car_model_price
        rental_price = float(car_model_price) * float(rental_days)
        rental = Rental.objects.create(
            car=car,
            client=request.user,
            start_date=from_date,
            end_date=to_date,
            rental_price=rental_price,  # calculate rental price
        )
        messages.success(request, 'Car rented successfully.')
        return redirect('home:client_rentals')

    context = {'car': car}
    return render(request, 'home/rent_car.html', context)


@login_required
def client_rentals(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if user_roles['is_owner']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('employee:index')
    rentals = Rental.objects.filter(client=request.user)
    context = {'rentals': rentals}
    return render(request, 'home/client_rentals.html', context)


def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {'car': car}
    return render(request, 'home/car_details.html', context)
