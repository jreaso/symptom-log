from django import forms
from .models import FormResponse

class FormResponseForm(forms.ModelForm):
    class Meta:
        model = FormResponse
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If a Form instance is associated with this FormResponse, filter the question choices accordingly.
        if self.instance.form:
            self.fields['question'].queryset = self.instance.form.questions.all()
