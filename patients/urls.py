from django.urls import path, include

from . import views
from forms.views import new_form_response_view

form_patterns = [
    path('<int:form_id>/submissions/new', new_form_response_view, name='new_form_response'),
]

urlpatterns = [
    path("", views.patients_list, name="patients_list"),
    path('<str:pk>/', views.patient_details, name='patient_details'),
    path('<str:pk>/forms/', include(form_patterns)),
]
