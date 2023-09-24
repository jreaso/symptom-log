from django.shortcuts import redirect
from django.http import HttpResponse
from authuser.models import Account

def index(request):
    # Check if the user is not logged in
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role in (Account.Role.ADMIN, Account.Role.CLINICIAN):
        return redirect('patients_list')
    
    elif request.user.role == Account.Role.PATIENT:
        return HttpResponse("Patient Logged In")
    
    return HttpResponse("Error: User does not have a role. Contact Admin.")
