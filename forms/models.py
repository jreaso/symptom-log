from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from authuser.models import Account


class Question(models.Model):
    question_title = models.CharField(max_length=50)
    label = models.CharField(max_length=30, null=True, blank=True)  # How this question should be labelled on graphs etc

    def __str__(self):
        if self.label:
            return self.label
        return self.question_title
    
    class Meta:
        abstract = True


class SymptomScoreQuestion(Question):
    pass


class TextQuestion(Question):
    pass


class MultipleChoiceQuestion(Question):
    options = models.CharField(null=True, blank=True)  # Store options as a comma-separated text


class StatusQuestion(Question):
    option_0 = models.CharField(max_length=10, null=True, blank=True)  # Label for False, Off, 0 etc
    option_1 = models.CharField(max_length=10, null=True, blank=True)  # Label for True, On, 1 etc


class EventQuestion(Question):
    pass


class Form(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    patient = models.ForeignKey(Account, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)

    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} - {self.title}"


class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    response_symptom_score = models.IntegerField(null=True, blank=True)
    response_multiple_choice_option = models.CharField(
        max_length=255, null=True, blank=True
    )
    response_text = models.TextField(null=True, blank=True)
    response_status = models.BooleanField(null=True, blank=True)
    response_event = models.CharField(max_length=255, null=True, blank=True)
    response_event_datetime = models.DateTimeField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.form} ({self.date_submitted})"

