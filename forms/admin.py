from django.contrib import admin
from .models import (
    Question,
    SymptomScoreQuestion, SymptomScoreResponse, 
    TextQuestion, TextResponse,
    MultipleChoiceQuestion, MultipleChoiceResponse,
    StatusQuestion, StatusResponse,
    EventQuestion, EventResponse, 
    Form, FormResponse
)

admin.site.register(Question)
admin.site.register(SymptomScoreQuestion)
admin.site.register(SymptomScoreResponse)
admin.site.register(TextQuestion)
admin.site.register(TextResponse)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceResponse)
admin.site.register(StatusQuestion)
admin.site.register(StatusResponse)
admin.site.register(EventQuestion)
admin.site.register(EventResponse)
admin.site.register(Form)
admin.site.register(FormResponse)
