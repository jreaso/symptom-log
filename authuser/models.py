import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, role="patient", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")

        if role == "admin":
            extra_fields.setdefault("is_staff", True)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("role") != "admin":
            raise ValueError("Superuser must be admin users.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=8, unique=True, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necessary when using AbstractBaseUser but not used
    is_superuser = models.BooleanField(default=False)

    class Role(models.TextChoices):
        PATIENT = "patient", "Patient"
        CLINICIAN = "clinician", "Clinician"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.role == "admin"

    def has_module_perms(self, app_label):
        return True
    
    def _generate_id():
        while True:
            random_uuid = str(uuid.uuid4()).replace("-", "")
            new_id = random_uuid[:8]

            if not Account.objects.filter(id=new_id).exists():
                return new_id
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = self._generate_id()
        super(Patient, self).save(*args, **kwargs)


class Patient(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)

    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=(("male", "Male"), ("female", "Female"), ("other", "Other")),
        null=True,
        blank=True,
    )


class Clinician(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    patients = models.ManyToManyField(Patient, related_name="clinicians", blank=True)


@receiver(post_save, sender=Account)
def create_user_role_model(sender, instance, created, **kwargs):
    if created:
        if instance.role.lower() == Account.Role.PATIENT:
            # Check if dob and sex exist in instance, otherwise use None
            dob = getattr(instance, "dob", None)
            sex = getattr(instance, "sex", None)
            Patient.objects.create(user=instance, dob=dob, sex=sex)
        elif instance.role.lower() == Account.Role.CLINICIAN:
            patients = getattr(instance, "patients", None)
            clinician = Clinician.objects.create(user=instance)
            if patients is not None:
                clinician.patients.set(patients)
