from django import forms
from .models import SymptomScoreResponse, TextResponse, MultipleChoiceResponse, StatusResponse, EventResponse, StatusQuestion, Form
from django.utils import timezone

class SymptomScoreResponseForm(forms.ModelForm):
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'step': 1})
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.label = None
            field.required = False

    class Meta:
        model = SymptomScoreResponse
        fields = ['score']

class TextResponseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False

    class Meta:
        model = TextResponse
        fields = ['text']

class MultipleChoiceResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False

        if self.question and hasattr(self.question, 'multiplechoicequestion'):
            choices = [(choice.strip(), choice.strip()) for choice in self.question.multiplechoicequestion.options.split(',')]
            self.fields['choice'].choices = choices

    choice = forms.ChoiceField(widget=forms.RadioSelect)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_choice(self):
        value = self.cleaned_data['choice']
        if value:
            if self.question:
                choices = [(choice.strip(), choice.strip()) for choice in self.question.multiplechoicequestion.options.split(',')]
                if value not in dict(choices).keys():
                    raise forms.ValidationError(f"Select a valid choice. {value} is not one of the available choices.")
        return value

    class Meta:
        model = MultipleChoiceResponse
        fields = ['choice']

class StatusResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        self.fields['status'].widget.attrs.update({'class': 'form-check-input'})

        if question:
            try:
                latest_response = StatusResponse.objects.filter(question=question).latest('form_response__submitted_at')
                self.fields['status'].initial = latest_response.status
            except StatusResponse.DoesNotExist:
                pass

            self.fields['status'].widget.attrs['option_0'] = question.statusquestion.option_0
            self.fields['status'].widget.attrs['option_1'] = question.statusquestion.option_1

    class Meta:
        model = StatusResponse
        fields = ['status']

class EventResponseForm(forms.ModelForm):
    event_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False
        #self.fields['event_datetime'].initial = timezone.now().replace(second=0, microsecond=0)

    class Meta:
        model = EventResponse
        fields = ['event_datetime']


class CreateNewFormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description']
