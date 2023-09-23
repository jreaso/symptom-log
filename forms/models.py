from django.db import models
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

class SymptomScoreResponse(models.Model):
    score = models.PositiveIntegerField()

    def __str__(self):
        return str(self.score)


class TextQuestion(Question):
    pass

class TextResponse(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class MultipleChoiceQuestion(Question):
    options = models.CharField(null=True, blank=True)  # Store options as a comma-separated text

class MultipleChoiceResponse(models.Model):
    choice = models.CharField(max_length=255)

    def __str__(self):
        return self.choice


class StatusQuestion(Question):
    option_0 = models.CharField(max_length=10, null=True, blank=True)  # Label for False, Off, 0 etc
    option_1 = models.CharField(max_length=10, null=True, blank=True)  # Label for True, On, 1 etc

class StatusResponse(models.Model):
    status = models.BooleanField()

    def __str__(self):
        return str(self.status)


class EventQuestion(Question):
    pass

class EventResponse(models.Model):
    event_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.event_datetime)


class Form(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    patient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='forms')
    questions = models.ManyToManyField(Question)

    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} - {self.title}"


class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    value = GenericForeignKey('content_type', 'object_id')

    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='submitted_responses')

    def __str__(self):
        return f"{self.form} ({self.date_submitted})"

