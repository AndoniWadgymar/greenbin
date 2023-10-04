from django.urls import path
from trash import views

app_name = 'trash'

urlpatterns = [
    path("", views.home, name='home'),
    path("<int:pk>/", views.TrashDetail.as_view(),name="details"),
    path("delete/<int:pk>", views.TrashDelete.as_view(), name="delete"),
    path("update/<int:pk>", views.TrashUpdate.as_view(), name="update"),
    path("all/", views.TrashList.as_view(), name="all" ),
    path("process/<int:pk>/<int:seconds>", views.process, name='process'),
    path("process/<int:pk>/completed/", views.process_completed, name="completed")
]
