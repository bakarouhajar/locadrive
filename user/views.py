from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from cities_light.models import City
from user.models import CustomUser, RoleEnum, Role

User = get_user_model()


def get_custom_user_roles(id):
    roles = {
        'is_client': False,
        'is_owner': False,
    }
    for role in CustomUser.objects.get(id=id).roles.values_list():
        if role[1] == RoleEnum.CLIENT.value:
            roles['is_client'] = True
            continue
        if role[1] == RoleEnum.OWNER.value:
            roles['is_owner'] = True
    return roles


def register_view(request):
    user = request.user
    if user.is_authenticated:
        user_roles = get_custom_user_roles(user.id)
        if user_roles['is_owner']:

            return redirect('employee:index')
        elif user_roles['is_client']:

            return redirect('home:index')

    cities = City.objects.all()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['register_as_owner']:
                user.roles.add(Role.objects.get(name=RoleEnum.OWNER.value))
            else:
                user.roles.add(Role.objects.get(name=RoleEnum.CLIENT.value))
            messages.success(request, 'Your account has been successfully created.')
            return redirect('home:index')
        else:
            return render(
                request,
                'user/register.html',
                {
                    'form': form,
                    'cities': cities,
                    'username': request.POST.get('username'),
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'phone': request.POST.get('phone'),
                    'city_id': int(request.POST.get('city')),
                    'email': request.POST.get('email'),
                }
            )
    return render(request, 'user/register.html', {'cities': cities})


def login_view(request):
    user = request.user
    if user.is_authenticated:
        user_roles = get_custom_user_roles(user.id)
        if user_roles['is_owner']:

            return redirect('employee:index')
        elif user_roles['is_client']:

            return redirect('home:index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'user/login.html', {
                'error_message': 'Sorry, Username and Password are required.',
            })
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'user/login.html', {
                'error_message': 'Sorry but your username or password is invalid.',
            })
        if not user.is_active:
            return render(request, 'user/login.html', {
                'error_message': 'Your account is deactivated, please contact administration.',
            })
        login(request, user)
        user_roles = get_custom_user_roles(user.id)
        if user.is_superuser:
            return redirect('admin:index')
        if user_roles['is_owner']:
            return redirect('employee:index')
        messages.success(request, 'Successful login.')
        return redirect('home:index')
    return render(request, 'user/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Successful logout')
        return redirect('home:index')

    messages.error(request, 'Unsuccessful logout')
    return redirect('home:index')


@login_required
def update_view(request):
    results = City.objects.all
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            user_roles = get_custom_user_roles(request.user.id)
            if user_roles['is_owner']:
                return redirect('/employee/')
            messages.success(request, f'Your account has been updated!')
            return redirect('user:profil')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
        "City": results,
    }
    return render(request, 'user/profil.html', context)
