from cities_light.forms import City
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms

from employee.models import Agency
from user.models import Role, RoleEnum, CustomUser

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    register_as_owner = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone',
            'city',
            'email',
            'password1',
            'password2',
            'picture',
        ]


class UserResetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = [
            'new_password1',
            'new_password2',
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'city']
