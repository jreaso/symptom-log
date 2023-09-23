from django.db import models
from authuser.models import Account


class Form(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    patient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='forms')

    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} - {self.title}"


class Question(models.Model):
    question_title = models.CharField(max_length=50)
    label = models.CharField(max_length=30, null=True, blank=True)  # How this question should be labelled on graphs etc
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        if self.label:
            return self.label
        return self.question_title


class Response(models.Model):
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='submitted_responses')

    def __str__(self):
        return f"{self.question} ({self.date_submitted})"


class SymptomScoreQuestion(Question):
    pass

class SymptomScoreResponse(Response):
    question = models.ForeignKey(SymptomScoreQuestion, on_delete=models.CASCADE, related_name='responses')
    score = models.PositiveIntegerField()


class TextQuestion(Question):
    pass

class TextResponse(Response):
    question = models.ForeignKey(TextQuestion, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()


class MultipleChoiceQuestion(Question):
    options = models.CharField(max_length=255, null=True, blank=True)  # Store options as a comma-separated text

class MultipleChoiceResponse(Response):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='responses')
    choice = models.CharField(max_length=255)


class StatusQuestion(Question):
    option_0 = models.CharField(max_length=10, null=True, blank=True)  # Label for False, Off, 0 etc
    option_1 = models.CharField(max_length=10, null=True, blank=True)  # Label for True, On, 1 etc

class StatusResponse(Response):
    question = models.ForeignKey(StatusQuestion, on_delete=models.CASCADE, related_name='responses')
    status = models.BooleanField()


class EventQuestion(Question):
    pass

class EventResponse(Response):
    question = models.ForeignKey(EventQuestion, on_delete=models.CASCADE, related_name='responses')
    event_datetime = models.DateTimeField()

