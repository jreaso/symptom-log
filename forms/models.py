from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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

    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    def save(self, *args, **kwargs):
        # Automatically assign the order when saving a new question
        if self.order is None:
            last_question = Question.objects.filter(form=self.form).order_by('-order').first()
            if last_question:
                self.order = last_question.order + 1
            else:
                self.order = 1
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        if self.label:
            return self.label
        return self.question_title
    

class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='form_responses')

    def __str__(self):
        return f"{self.form} ({self.submitted_at})"


class Response(models.Model):
    form_response = models.ForeignKey(FormResponse, on_delete=models.CASCADE, null=True, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return f"{self.question} ({self.form_response.submitted_at})"


class SymptomScoreQuestion(Question):
    pass

class SymptomScoreResponse(Response):
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True, blank=True
    )


class TextQuestion(Question):
    pass

class TextResponse(Response):
    text = models.TextField(null=True, blank=True)


class MultipleChoiceQuestion(Question):
    options = models.CharField(max_length=255)  # Store options as a comma-separated text

class MultipleChoiceResponse(Response):
    choice = models.CharField(max_length=255, null=True, blank=True)


class StatusQuestion(Question):
    option_0 = models.CharField(max_length=10, null=True, blank=True)  # Label for False, Off, 0 etc
    option_1 = models.CharField(max_length=10, null=True, blank=True)  # Label for True, On, 1 etc

class StatusResponse(Response):
    status = models.BooleanField()


class EventQuestion(Question):
    pass

class EventResponse(Response):
    event_datetime = models.DateTimeField(null=True, blank=True)

