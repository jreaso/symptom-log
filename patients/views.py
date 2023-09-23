from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
#from core.models import Patient, Account


@login_required
def patients_list(request):
    if request.user.role in ["admin", "clinician"]:
        if request.user.role == "admin":
            #patients = Patient.objects.all()
            patients = None
        else:
            # For clinicians, display only their related patients
            patients = request.user.clinician.patients.all()
        
        return render(request, "patients/patient_list.html", {"patients": patients})
    else:
        raise PermissionDenied
