from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from forms.models import FormResponse
from authuser.models import Account
from django.core.exceptions import PermissionDenied

def dashboard_view(request):

    if request.user.role == Account.Role.PATIENT:
        return render(request, "dashboard/main_dashboard.html")
    else:
        return HttpResponseForbidden()
