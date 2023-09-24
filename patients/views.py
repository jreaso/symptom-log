from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from authuser.models import Account, Patient, Clinician


@login_required
def patients_list(request):
    if request.user.role in [Account.Role.ADMIN, Account.Role.CLINICIAN]:
        if request.user.role == Account.Role.ADMIN:
            patients = Patient.objects.all()
        elif request.user.role == Account.Role.CLINICIAN:
            patients = request.user.clinician.patients.all()
        return render(request, "patients/patients_list.html", {"patients": patients})
    else:
        raise PermissionDenied
    

@login_required
def patient_details(request, pk):
    # get patient object
    patient = get_object_or_404(Patient, pk=pk)
    patient_forms = patient.user.forms.all()

    context = {'patient': patient, 'patient_forms': patient_forms}

    if request.user.role == Account.Role.ADMIN:
        return render(request, "patients/patient_details.html", context)
    elif request.user.role == Account.Role.CLINICIAN:
        clinician = request.user.clinician
        if patient in clinician.patients.all():
            #return HttpResponse("Patient Page")
            return render(request, "patients/patient_details.html", context)
        else:
            return HttpResponse("Patient Is Not Registered With You")
    else:
        raise PermissionDenied
