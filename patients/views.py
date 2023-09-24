from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
