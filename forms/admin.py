from django.contrib import admin
from .models import (
    SymptomScoreQuestion,
    SymptomScoreResponse,
    TextQuestion,
    TextResponse,
    MultipleChoiceQuestion,
    MultipleChoiceResponse,
    StatusQuestion,
    StatusResponse,
    EventQuestion,
    EventResponse,
    Form,
    FormResponse,
)

# Define admin classes for each model
@admin.register(SymptomScoreQuestion)
class SymptomScoreQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'label')

@admin.register(SymptomScoreResponse)
class SymptomScoreResponseAdmin(admin.ModelAdmin):
    list_display = ('score',)

@admin.register(TextQuestion)
class TextQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'label')

@admin.register(TextResponse)
class TextResponseAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'label')

@admin.register(MultipleChoiceResponse)
class MultipleChoiceResponseAdmin(admin.ModelAdmin):
    list_display = ('choice',)

@admin.register(StatusQuestion)
class StatusQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'label')

@admin.register(StatusResponse)
class StatusResponseAdmin(admin.ModelAdmin):
    list_display = ('status',)

@admin.register(EventQuestion)
class EventQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'label')

@admin.register(EventResponse)
class EventResponseAdmin(admin.ModelAdmin):
    list_display = ('event_datetime',)

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'date_created', 'last_edited')
    filter_horizontal = ('questions',)  # Use a filter_horizontal widget for the questions field

@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'question', 'submitted_at', 'submitted_by')

