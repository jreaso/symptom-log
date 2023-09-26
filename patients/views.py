from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from authuser.models import Account, Patient, Clinician
from forms.models import FormResponse


@login_required
def patients_list(request):
    if request.user.role in [Account.Role.ADMIN, Account.Role.CLINICIAN]:
        if request.user.role == Account.Role.ADMIN:
            patients = Patient.objects.all()
        elif request.user.role == Account.Role.CLINICIAN:
            patients = request.user.clinician.patients.all()

        patients_with_dates = []
        for patient in patients:
            latest_form_response = FormResponse.objects.filter(form__patient=patient.user).order_by('-submitted_at').first()
            if latest_form_response:
                patients_with_dates.append((patient, latest_form_response.submitted_at))
            else:
                patients_with_dates.append((patient, "No forms"))
        
        context = {
            "patients_with_dates": patients_with_dates,
            'user': request.user
        }

        return render(request, "patients/patients_list.html", context)
    else:
        raise PermissionDenied
    

@login_required
def patient_details(request, pk):
    # get patient object
    patient = get_object_or_404(Patient, pk=pk)
    patient_forms = patient.user.forms.all()

    patient_forms_details = []

    for form in patient_forms:
        last_response = form.responses.order_by('-submitted_at').first()
        last_response_date = last_response.submitted_at if last_response else None

        patient_forms_details.append((form, last_response_date))
    
    form_responses = FormResponse.objects.filter(form__patient=patient.user).order_by('-submitted_at')

    context = {
        'patient': patient,
        'patient_forms': patient_forms_details,
        'form_responses': form_responses
    }

    if request.user.role == Account.Role.ADMIN:
        return render(request, "patients/patient_details.html", context)
    elif request.user.role == Account.Role.CLINICIAN:
        clinician = request.user.clinician
        if patient in clinician.patients.all():
            return render(request, "patients/patient_details.html", context)
        else:
            return HttpResponse("Patient Is Not Registered With You")
    else:
        raise PermissionDenied
