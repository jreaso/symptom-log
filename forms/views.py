from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Form, FormResponse
from .forms import SymptomScoreResponseForm, TextResponseForm, MultipleChoiceResponseForm, StatusResponseForm, EventResponseForm
from django.contrib.auth.decorators import login_required


@login_required
def form_response_view(request):
    form_instance = Form.objects.first()  # Temporary for testing
    response_forms_questions = []

    if request.method == 'POST':
        for question in form_instance.questions.all():
            form_class, question_form_instance = _get_form_for_question(question)
            if form_class:
                response_form = form_class(request.POST, prefix=str(question.id), question=question)
                response_forms_questions.append((response_form, question))
        
        if all([response_form.is_valid() for response_form, question in response_forms_questions]):
            form_response = FormResponse(form=form_instance, submitted_by=request.user)
            form_response.save()

            for response_form, question in response_forms_questions:
                response_instance = response_form.save(commit=False)
                response_instance.form_response = form_response
                response_instance.question = question
                response_instance.save()
        
        else:
            print("INVALID RESPONSE!")
        
        form_response = FormResponse(form=form_instance, submitted_by=request.user)
        form_response.save()

        return HttpResponse("Success")  # Temporary for testing - should route to view the responses page
    
    context = {
        'form_instance': form_instance,
        'form_response_forms': [
            (question, form_class, form_instance) for question, (form_class, form_instance) in 
            [(q, _get_form_for_question(q)) for q in form_instance.questions.all()]
        ]
    }

    return render(request, 'forms/form_response.html', context)



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


