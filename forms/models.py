from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from authuser.models import Account


class Form(models.Model):
    patient = models.OneToOneField(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    questions = models.ManyToManyField("Question", blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    question_title = models.CharField(max_length=50)
    label = models.CharField(max_length=30, null=True, blank=True)  # How this question should be labelled on graphs etc

    class QuestionType(models.TextChoices):
        SYMPTOM_SCORE = "symptom_score", "Symptom Score"  # 1-10 score
        MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"  # MC question
        TEXT = "text", "Text"  # Plain text response
        STATUS = "status", "Status"  # Status e.g. On/Off
        EVENT = "event", "Event"  # Date and activity e.g. Back Physio

    question_type = models.CharField(max_length=15, choices=QuestionType.choices)

    def __str__(self):
        if self.label:
            return self.label
        return self.question_title


class MultipleChoiceQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    options = models.CharField(null=True, blank=True)  # Store options as a comma-separated text

    def __str__(self):
        return f"{self.question}, Options"


class StatusQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    option_0 = models.CharField(max_length=10, null=True, blank=True)  # Label for False/Off/0 etc
    option_1 = models.CharField(max_length=10, null=True, blank=True)  # Label for True/On/1 etc

    def __str__(self):
        return f"{self.question}, Options"


class EventQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    event = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.event}"


class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    patient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='form_response_patient')

    response_symptom_score = models.IntegerField(null=True, blank=True)
    response_multiple_choice_option = models.CharField(
        max_length=255, null=True, blank=True
    )
    response_text = models.TextField(null=True, blank=True)
    response_status = models.BooleanField(null=True, blank=True)
    response_event = models.CharField(max_length=255, null=True, blank=True)
    response_event_datetime = models.DateTimeField(null=True, blank=True)

    date_submitted = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='form_response_submitted_by')

    def __str__(self):
        return f"{self.patient} - {self.form} ({self.date_submitted})"


@receiver(post_save, sender=Question)
def create_question_type(sender, instance, created, **kwargs):
    if created:
        if instance.question_type == Question.QuestionType.MULTIPLE_CHOICE:
            # Check if options exist in instance, otherwise use None
            options = getattr(instance, "options", None)
            MultipleChoiceQuestion.objects.create(question=instance, options=options)

        elif instance.question_type == Question.QuestionType.STATUS:
            # Check if option_0 and option_1 exist in instance, otherwise use None
            option_0 = getattr(instance, "option_0", None)
            option_1 = getattr(instance, "option_1", None)
            StatusQuestion.objects.create(
                question=instance, option_0=option_0, option_1=option_1
            )

        elif instance.question_type == Question.QuestionType.EVENT:
            # Check if event and date exist in instance, otherwise use None
            event = getattr(instance, "event", None)
            EventQuestion.objects.create(question=instance, event=event)
