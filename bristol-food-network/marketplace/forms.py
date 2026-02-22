from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label='First name')
    last_name = forms.CharField(max_length=30, required=False, label='Last name')
    email = forms.EmailField(required=False, label='Email address')
    phone = forms.CharField(max_length=20, required=False, label='Phone number')
    delivery_address = forms.CharField(max_length=300, required=False, label='Delivery address')
    postcode = forms.CharField(max_length=10, required=False, label='Postcode')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
