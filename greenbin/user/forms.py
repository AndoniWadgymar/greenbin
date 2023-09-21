from typing import Any
from django import forms
from user.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profileimg', 'bio', 'location']