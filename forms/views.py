from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Form, FormResponse, SymptomScoreQuestion, TextQuestion, MultipleChoiceQuestion, StatusQuestion, EventQuestion
from .forms import SymptomScoreResponseForm, TextResponseForm, MultipleChoiceResponseForm, StatusResponseForm, EventResponseForm

def form_response_view(request):
    form_instance = Form.objects.first()

    if request.method == 'POST':
        print(request.POST)
        form_response = FormResponse(form=form_instance, submitted_by=request.user)
        form_response.save()

        for question in form_instance.questions.all():
            form_class, form_instance = _get_form_for_question(question)  # Unpack the tuple here
            if form_class:  # Only process if we found a valid form class for the question
                response_form = form_class(request.POST, prefix=str(question.id))
                if response_form.is_valid():
                    response_instance = response_form.save(commit=False)
                    print(f"Question being assigned to response: {question.id}")
                    response_instance.form_response = form_response
                    response_instance.question = question
                    response_instance.save()
                else: #DELETE
                    print(f"Form errors for question {question.id}: {response_form.errors}")

        return HttpResponse("Success")  # You can replace 'some-success-url' with a real URL


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
            return (StatusResponseForm, StatusResponseForm(prefix=str(question.id)))
        elif hasattr(question, 'eventquestion'):
            return (EventResponseForm, EventResponseForm(prefix=str(question.id)))
    except Exception as e:
        print(f"Error with question {question.id}: {e}")
    return (None, None)


