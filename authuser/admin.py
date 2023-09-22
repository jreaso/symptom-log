from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from authuser.models import Account, Patient, Clinician

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'date_joined', 'last_login', 'is_staff', 'role_info')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    ordering = ()

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'role', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('patient', 'clinician')

    def role_info(self, obj):
        if obj.role == 'patient' and hasattr(obj, 'patient'):
            return f"DOB: {obj.patient.dob}, Sex: {obj.patient.sex}"
        elif obj.role == 'clinician' and hasattr(obj, 'clinician'):
            return f"Patients: {', '.join([str(patient) for patient in obj.clinician.patients.all()])}"
        return "No Info"

    role_info.short_description = "Role Info"

class PatientAdmin(ModelAdmin):
    list_display = ('user', 'dob', 'sex')
    search_fields = ()
    filter_horizontal = ()

class ClinicianAdmin(ModelAdmin):
    list_display = ('user', 'list_of_patients')
    search_fields = ()

    def list_of_patients(self, obj):
        return ", ".join([str(patient) for patient in obj.patients.all()])

    list_of_patients.short_description = "Patients"

admin.site.register(Account, AccountAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Clinician, ClinicianAdmin)
