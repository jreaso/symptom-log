from django.contrib import admin
from .models import Form, Question, MultipleChoiceQuestion, StatusQuestion, EventQuestion, FormResponse
from .forms import FormResponseForm

@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    form = FormResponseForm

# Register other models with the admin interface
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(StatusQuestion)
admin.site.register(EventQuestion)
