from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from authuser.models import Patient, Account


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
    patient = get_object_or_404(Patient, pk=pk)
    # Add any additional context data you need for the detail view
    #context = {'patient': patient}
    return HttpResponse("Patient Details Page")
    #return render(request, 'patients/patient_detail.html', context)
