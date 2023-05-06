from django import forms
from django.core.exceptions import ValidationError
from .models import Car, CarModel, Agency


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['agency', 'is_active']


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_brand'].widget.attrs['class'] = 'form-select'


class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'email', 'phone', 'address', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }
