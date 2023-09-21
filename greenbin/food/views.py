from typing import Any, Dict
from django.shortcuts import redirect, render, get_object_or_404

# Import Django generic Views for Create, Update, Delete, List and Detail
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

# Import Models from food.model
from food.models import Food, Category
from food.forms import FoodForm
import requests
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
# from food.forms import FoodForm

class FoodList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"    
    model = Food
    queryset = Food.objects.order_by('name')
    context_object_name = 'foods'

    def get_queryset(self):
        filter_val = self.request.GET.get('category')
        if filter_val:
            new_context = Food.objects.filter(category=filter_val)
        else:
            new_context = Food.objects.all()
        return new_context
    
class FoodDetail(LoginRequiredMixin, DetailView):
    model = Food

    def get_context_data(self, *args, **kwargs):
        #Get data from view
        context = super(FoodDetail, self).get_context_data(*args, **kwargs)
        # add extra field
        food = context['object']
        API_KEY = 'Dp9XFa8CxLDJZsf0vKxeHN95Lfsen3EFzn62vXpH'
        
        try:
            response = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={food}&dataType=Foundation&pageSize=1')
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
             raise SystemExit(err)
        
        search_data = response.json()
        fdcid = search_data['foods'][0]['fdcId']

        try:
            response = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{fdcid}?api_key={API_KEY}')
        except requests.exceptions.HTTPError as err:
             raise SystemExit(err)
        
        especific_data = response.json()
        food_nutrients = especific_data['foodNutrients']

        # Code to create a dictionary with all the nutrients and their values
        food_nut = []
        aux = {}
        for nutrient in food_nutrients:
            if 'foodNutrientDerivation' not in nutrient:
                food_nut.append(aux)
                aux = nutrient['nutrient']['name']
                food_nut.append(aux)
                aux = {}
            else:
                aux[f"{nutrient['nutrient']['name']}"] = str(nutrient['amount']) + nutrient['nutrient']['unitName']
        food_nut.append(aux)
        food_nut.pop(0)

        # Code to formate the two dicts that will be sent
        classes = []
        nutrient_elements = []
        for i in range(len(food_nut)):
            if i%2==0:
                classes.append(food_nut[i])
            else:
                nutrient_elements.append(food_nut[i])
        
        zippedList = zip(classes, nutrient_elements)
        context["zippedList"] = zippedList
        return context
    
class FoodCreate(LoginRequiredMixin, CreateView):
    model = Food
    fields = ['name', 'weight', 'image','category', 'created_by']
    success_url = "/food/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class FoodDelete(DeleteView):
    model = Food
    success_url = reverse_lazy('food:foods')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
