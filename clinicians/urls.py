from django.urls import path
from . import views

urlpatterns = [
    path("", views.clinicians_list, name="clinicians_list"),
]
