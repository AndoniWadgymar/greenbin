from typing import Any
from django.conf import settings
from django.forms import ModelForm, TextInput
from trash.models import Trash

class TrashForm(ModelForm):
    # Fields we want to add to usercreation default form
    class Meta:
        model = Trash
        fields = ['size', 'user_size', 'user_duration', 'foods']
        widgets = {'user_size' : TextInput(attrs={'placeholder': 'Weight in grams'}),
            'user_duration': TextInput(attrs={'placeholder': 'Format("HH:mm:ss")'})}

