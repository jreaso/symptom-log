from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Form, FormResponse, Response
from .forms import SymptomScoreResponseForm, TextResponseForm, MultipleChoiceResponseForm, StatusResponseForm, EventResponseForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from authuser.models import Account
from datetime import datetime, timedelta
from .forms import CreateNewFormForm


@login_required
def new_form_response_view(request, pk, form_id):
    patient = get_object_or_404(Account, pk=pk)
    form_instance = get_object_or_404(Form, id=form_id, patient=patient)

    response_forms_questions = []

    if request.method == 'POST':
        for question in form_instance.questions.all().order_by('order'):
            form_class, question_form_instance = _get_form_for_question(question)
            if form_class:
                response_form = form_class(request.POST, prefix=str(question.id), question=question)
                response_forms_questions.append((response_form, question))
        
        if all([response_form.is_valid() for response_form, question in response_forms_questions]):
            form_response = FormResponse(form=form_instance)
            form_response.submitted_by = request.user
            form_response.save()

            for response_form, question in response_forms_questions:
                if all(value is not None and value != "" for value in response_form.cleaned_data.values()):
                    response_instance = response_form.save(commit=False)
                    response_instance.form_response = form_response
                    response_instance.question = question
                    response_instance.save()
        
        else:
            print(f"INVALID RESPONSE! {[response_form.is_valid() for response_form, question in response_forms_questions]}")
            raise ValidationError("Invalid Form Response")

        response_datetime_str = form_response.submitted_at.strftime('%Y%m%d%H%M%S')
        return redirect('form_response', pk=form_response.form.patient.id, form_id=form_response.form.id, response_datetime=response_datetime_str)
    
    context = {
        'form_instance': form_instance,
        'form_response_forms': [
            (question, form_class, form_instance) for question, (form_class, form_instance) in 
            [(q, _get_form_for_question(q)) for q in form_instance.questions.all().order_by('order')]
        ],
        'user': request.user
    }

    return render(request, 'forms/form_response_new.html', context)



def _get_form_for_question(question):
    try:
        if hasattr(question, 'symptomscorequestion'):
            return (SymptomScoreResponseForm, SymptomScoreResponseForm(prefix=str(question.id)))
        elif hasattr(question, 'textquestion'):
            return (TextResponseForm, TextResponseForm(prefix=str(question.id)))
        elif hasattr(question, 'multiplechoicequestion'):
            return (MultipleChoiceResponseForm, MultipleChoiceResponseForm(prefix=str(question.id), question=question))
        elif hasattr(question, 'statusquestion'):
            return (StatusResponseForm, StatusResponseForm(prefix=str(question.id), question=question))
        elif hasattr(question, 'eventquestion'):
            return (EventResponseForm, EventResponseForm(prefix=str(question.id)))
    except Exception as e:
        print(f"Error with question {question.id}: {e}")
    return (None, None)


@login_required
def form_response_view(request, pk, form_id, response_datetime):
    patient = get_object_or_404(Account, pk=pk)
    form_instance = get_object_or_404(Form, id=form_id, patient=patient)

    submitted_at_start = datetime.strptime(response_datetime, '%Y%m%d%H%M%S')
    submitted_at_end = submitted_at_start + timedelta(seconds=1)
    form_response = get_object_or_404(
        FormResponse,
        form=form_instance,
        submitted_at__gte=submitted_at_start,
        submitted_at__lt=submitted_at_end
    )

    question_responses = Response.objects.filter(form_response=form_response).order_by('question__order')

    context = {
        'form_instance': form_instance,
        'form_response': form_response,
        'question_responses': question_responses,
        'user': request.user
    }

    return render(request, 'forms/form_response.html', context)


@login_required
def form_responses_list_view(request, pk, form_id):
    patient = get_object_or_404(Account, pk=pk)
    form_instance = get_object_or_404(Form, id=form_id, patient=patient)

    form_responses = FormResponse.objects.filter(form=form_instance).order_by('-submitted_at')
    
    context ={ 
        'form_instance': form_instance,
        'form_responses': form_responses,
        'patient': patient
    }
    return render(request, 'forms/form_responses_list.html', context)


def create_new_form(request, pk):

    if request.method == 'POST':
        form = CreateNewFormForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.patient = Account.objects.get(id=pk)
            new_form.save()
            return HttpResponseRedirect('#')  # redirect to #

    # If there's any other situation, just redirect back to '#'.
    return HttpResponseRedirect('#')