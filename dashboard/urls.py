from django.urls import path, include

from . import views
from forms.views import new_form_response_view, form_response_view, form_responses_list_view, forms_list_view

patient_form_submission_patterns = [
    path('new', new_form_response_view, name='new_form_response_patient'),
    path('<str:response_datetime>/', form_response_view, name='form_response_patient'),
]

patient_form_patterns = [
    path('', forms_list_view, name='forms_list'),
    path('<int:form_id>/submissions/', include(patient_form_submission_patterns)),
    path('<int:form_id>/', form_responses_list_view, name='form_responses_list_patient'),
]

urlpatterns = [
    path("dashboard", views.dashboard_view, name="dashboard"),
    path('forms/', include(patient_form_patterns)),
]
