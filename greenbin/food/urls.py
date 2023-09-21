from django.urls import path
from food import views

app_name = 'food'

urlpatterns = [
    path("", views.FoodList.as_view(), name="foods" ),
    path("<int:pk>/",views.FoodDetail.as_view(),name="details"),
    path("create/", views.FoodCreate.as_view(), name="create"),
    path("delete/<int:pk>", views.FoodDelete.as_view(), name="delete"),
] 
