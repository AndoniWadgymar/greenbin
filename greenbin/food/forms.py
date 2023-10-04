from food.models import Food
from django.forms import ModelForm, TextInput, IntegerField, ImageField, Textarea

class FoodForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Food
        fields = ['name', 'name_eng', 'weight', 'category']
