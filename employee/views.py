from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from user.models import CustomUser, Role, RoleEnum
from user.views import get_custom_user_roles
from .forms import CarForm, AgencyForm
from employee.models import Car
from django.db.models import Sum, Count
from django.shortcuts import render
from django.utils import timezone
from .models import Rental


def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if user.is_superuser:
        return redirect('/admin/')
    if not user_roles['is_owner']:
        return redirect('home:index')
    agency = user.agency
    cars = Car.objects.filter(agency=agency)
    users = CustomUser.objects. \
        exclude(is_superuser=True). \
        exclude(is_staff=True). \
        exclude(roles__in=Role.objects.filter(
        name__in=(
            RoleEnum.OWNER.value,
        )
    )
    )
    context = {
        'cars': cars,
        'is_owner': user_roles['is_owner'],
    }
    return render(request, 'employee/index.html', context)


def add_car(request):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if user.is_superuser:
        return redirect('/admin/')
    if not user_roles['is_owner']:
        return redirect('home:index')
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        car = form.save(commit=False)
        car.agency = request.user.agency
        car.save()
        messages.success(request, "Car added successfully!")
        return redirect('employee:cars')
    return render(request, 'employee/add_car.html', {'form': form})


def cars(request):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if user.is_superuser:
        return redirect('/admin/')
    if not user_roles['is_owner']:
        return redirect('home:index')

    cars = Car.objects.filter(agency=user.agency)

    context = {
        'cars': cars,
    }
    return render(request, 'employee/cars.html', context)


@login_required
def rental_income(request, car_id):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    car = get_object_or_404(Car, id=car_id)
    rental_income = Rental.objects.filter(car=car, paid=True).aggregate(Sum('rental_price'))
    total_income = rental_income['rental_price__sum'] or 0
    context = {'car': car, 'total_income': total_income}
    return render(request, 'employee/rental_income.html', context)


def update_car(request, car_id):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Car has been updated successfully.")
            return redirect('employee:cars')
    else:
        form = CarForm(instance=car)
    context = {
        'form': form,
        'car': car,
    }
    return render(request, 'employee/update_car.html', context)


def delete_car(request, car_id):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        messages.add_message(request, messages.INFO, 'Car has been deleted.')
        return redirect('employee:cars')
    context = {
        'car': car,
    }
    return render(request, 'employee/delete_car.html', context)


def detail_car(request, car_id):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    car = get_object_or_404(Car, id=car_id)
    context = {'car': car}
    return render(request, 'employee/detail_car.html', context)


@login_required
def rentals(request):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_owner']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home:index')

    agency = user.agency
    cars = Car.objects.filter(agency=agency)
    rentals = Rental.objects.filter(car__in=cars)

    context = {
        'cars': cars,
        'rentals': rentals,
        'is_owner': user_roles['is_owner'],
    }
    return render(request, 'employee/rentals.html', context)


@require_POST
def update_rental(request):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    rental_id = request.POST.get('rental_id')
    is_paid = request.POST.get('is_paid') == 'true'
    is_confirmed = request.POST.get('is_confirmed') == 'true'

    rental = Rental.objects.get(id=rental_id)
    rental.paid = is_paid
    rental.confirmed = is_confirmed
    rental.save()

    return JsonResponse({'success': 'Rental updated successfully'})


@login_required
def rental_income(request):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    agency = request.user.agency
    rentals = Rental.objects.filter(car__agency=agency, paid=True)

    total_income = rentals.aggregate(total_income=Sum('rental_price'))['total_income'] or 0

    start_date = rentals.order_by('start_date').first().start_date if rentals.exists() else timezone.now().date()
    end_date = rentals.order_by('-end_date').first().end_date if rentals.exists() else timezone.now().date()

    months_diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    per_month_income = total_income / months_diff if months_diff > 0 else 0

    top_rented_car = rentals.values('car__car_model__name', 'car__car_model__car_brand__name') \
        .annotate(total_rentals=Count('id')) \
        .order_by('-total_rentals') \
        .first()
    topcar_profit = rentals.values('car__car_model__name',
                                   'car__car_model__car_brand__name').annotate(
        total_rental_price=Sum('rental_price')).order_by('-total_rental_price').first()
    context = {
        'total_income': total_income,
        'per_month_income': per_month_income,
        'top_rented_car': top_rented_car,
        'topcar_profit': topcar_profit,
    }

    return render(request, 'employee/rental_income.html', context)


@login_required
def owner_profile(request):
    agency = request.user.agency
    context = {
        'user': request.user,
        'agency': agency,
    }
    return render(request, 'employee/owner_profile.html', context)


@login_required
def detail_client(request, client_id):
    if request.user.agency is None:
        # Redirect to a different view, or display an error message
        messages.error(request, "You need to register your agency first.")
        return redirect('employee:agency')
    user = request.user
    if not user.is_authenticated:
        return redirect('user:login')
    user_roles = get_custom_user_roles(request.user.id)
    if not user_roles['is_owner']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home:index')
    client = get_object_or_404(CustomUser, id=client_id)
    context = {'client': client}
    return render(request, 'employee/detail_client.html', context)


def agency_view(request):
    if request.user.agency is not None:
        # Redirect to a different view, or display an error message
        return redirect('employee:owner_profile')
    if request.method == 'POST':
        form = AgencyForm(request.POST)
        if form.is_valid():
            agency = form.save()
            # Link the agency to the current user's agency field
            request.user.agency = agency
            request.user.save()
            # Redirect to a success page
            return redirect('employee:owner_profile')
    else:
        form = AgencyForm()
    return render(request, 'employee/agency.html', {'form': form})
