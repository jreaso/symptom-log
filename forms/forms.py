from django import forms
from .models import SymptomScoreResponse, TextResponse, MultipleChoiceResponse, StatusResponse, EventResponse

class SymptomScoreResponseForm(forms.ModelForm):
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'class': 'form-control'})
    )

    class Meta:
        model = SymptomScoreResponse
        fields = ['score']

class TextResponseForm(forms.ModelForm):
    class Meta:
        model = TextResponse
        fields = ['text']

class MultipleChoiceResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        if question and hasattr(question, 'multiplechoicequestion'):
            choices = [(choice.strip(), choice.strip()) for choice in question.multiplechoicequestion.options.split(',')]
            self.fields['choice'].choices = choices

    choice = forms.ChoiceField(widget=forms.RadioSelect)

    class Meta:
        model = MultipleChoiceResponse
        fields = ['choice']

class StatusResponseForm(forms.ModelForm):
    class Meta:
        model = StatusResponse
        fields = ['status']

class EventResponseForm(forms.ModelForm):
    event_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = EventResponse
        fields = ['event_datetime']
