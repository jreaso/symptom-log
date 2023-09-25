from django import forms
from .models import SymptomScoreResponse, TextResponse, MultipleChoiceResponse, StatusResponse, EventResponse

class SymptomScoreResponseForm(forms.ModelForm):
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)  # It pops and ignores the 'question' argument
        super().__init__(*args, **kwargs)

    class Meta:
        model = SymptomScoreResponse
        fields = ['score']

class TextResponseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)  # It pops and ignores the 'question' argument
        super().__init__(*args, **kwargs)

    class Meta:
        model = TextResponse
        fields = ['text']

class MultipleChoiceResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        if self.question and hasattr(self.question, 'multiplechoicequestion'):
            choices = [(choice.strip(), choice.strip()) for choice in self.question.multiplechoicequestion.options.split(',')]
            print(f"Setting choices for question {self.question.id}: {choices}")
            self.fields['choice'].choices = choices

    choice = forms.ChoiceField(widget=forms.RadioSelect)

    def clean(self):
        cleaned_data = super().clean()
        print(f"Form-wide validation errors for question {self.question.id}: {self.errors}")
        return cleaned_data

    def clean_choice(self):
        value = self.cleaned_data['choice']
        if self.question:
            choices = [(choice.strip(), choice.strip()) for choice in self.question.multiplechoicequestion.options.split(',')]
            print(f"Choices during validation for question {self.question.id}: {choices}")
            if value not in dict(choices).keys():
                raise forms.ValidationError(f"Select a valid choice. {value} is not one of the available choices.")
        return value

    class Meta:
        model = MultipleChoiceResponse
        fields = ['choice']

class StatusResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)  # It pops and ignores the 'question' argument
        super().__init__(*args, **kwargs)

    class Meta:
        model = StatusResponse
        fields = ['status']

class EventResponseForm(forms.ModelForm):
    event_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('question', None)  # It pops and ignores the 'question' argument
        super().__init__(*args, **kwargs)

    class Meta:
        model = EventResponse
        fields = ['event_datetime']
