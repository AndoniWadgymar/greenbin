from typing import Any
from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # Fields we want to add to usercreation default form
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        widgets = {'user_size' : TextInput(attrs={'placeholder': 'Weight in grams'}),
            'user_duration': TextInput(attrs={'placeholder': 'Format("HH:mm:ss")'})}