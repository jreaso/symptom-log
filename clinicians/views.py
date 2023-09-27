from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from authuser.models import Account, Patient, Clinician


@login_required
def clinicians_list(request):
    if request.user.role == Account.Role.ADMIN:
        clinicians = Clinician.objects.all()

        clinicians_patients = []

        for clinician in clinicians:
            patients = clinician.patients.all()
            clinicians_patients.append((clinician, patients))
        
        context = {
            "clinicians_patients": clinicians_patients,
            'user': request.user
        }

        return render(request, "clinicians/clinicians_list.html", context)
    else:
        raise PermissionDenied
    