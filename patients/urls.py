from django.urls import path

from . import views

urlpatterns = [
    path("", views.patients_list, name="patients_list"),
]