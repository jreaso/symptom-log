from django.urls import path, include

from . import views
from forms.views import new_form_response_view, form_response_view, form_responses_list_view, create_new_form, edit_form_view, delete_question_view, edit_question_view, add_question_view, delete_form_view

form_submission_patterns = [
    path('new', new_form_response_view, name='new_form_response'),
    path('<str:response_datetime>/', form_response_view, name='form_response'),
]

form_edit_patterns = [
    path('', edit_form_view, name='edit_form'),
    path('<int:question_id>/delete/', delete_question_view, name='delete_question'),
    path('<int:question_id>/edit/', edit_question_view, name='edit_question'),
    path('add', add_question_view, name='add_question')
]

form_patterns = [
    path('<int:form_id>/submissions/', include(form_submission_patterns)),
    path('<int:form_id>/edit/', include(form_edit_patterns)),
    path('<int:form_id>/', form_responses_list_view, name='form_responses_list'),
    path('<int:form_id>/delete', delete_form_view, name='delete_form'),
    path('new/', create_new_form, name='create_new_form')
]

urlpatterns = [
    path("", views.patients_list, name="patients_list"),
    path('<str:pk>/', views.patient_details, name='patient_details'),
    path('<str:pk>/forms/', include(form_patterns)),
]
