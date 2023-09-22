from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, role='patient', **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        
        if role == 'admin':
            extra_fields.setdefault("is_staff", True)
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        # Create associated Patient or Clinician object based on the role
        if role.lower() == 'patient':
            Patient.objects.create(user=user, dob=extra_fields.get('dob'), sex=extra_fields.get('sex'))
        elif role.lower() == 'clinician':
            Clinician.objects.create(user=user)
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("role", 'admin')
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("role") != 'admin':
            raise ValueError("Superuser must be admin users.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    #username = models.CharField(verbose_name="username", max_length=30, unique=True)
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
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.role == 'admin'
    
    def has_module_perms(self, app_label):
        return True
 

class Patient(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    #patient_id = models.IntegerField(null=True, blank=True)
    dob = models.DateField()
    sex = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))

class Clinician(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    patients = models.ManyToManyField(Patient, related_name='clinicians')

