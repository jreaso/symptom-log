from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Account


def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        email = request.POST["email"]
        password = request.POST["password"]

        if not email:
            return render(
                request,
                "authuser/login.html",
                {"title": "Login", "message": "Please Enter Email"},
            )

        if not password:
            return render(
                request,
                "authuser/login.html",
                {"title": "Login", "message": "Please Enter Password"},
            )
        
        if not Account.objects.filter(email=email).exists():
            return render(
                request,
                "authuser/login.html",
                {"title": "Login", "message": "Account Does Not Exist", "email": email},
            )

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, email=email, password=password)

        # If user object is returned, log in and route to index page:
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(
                request,
                "authuser/login.html",
                {"title": "Login", "message": "Invalid Credentials", "email": email},
            )
    else:
        # Check if user is already logged in
        if request.user.is_authenticated:
            return HttpResponse("Logged In")
        else:
            return render(request, "authuser/login.html", {"title": "Login"})


def logout_view(request):
    logout(request)
    return render(
        request, "authuser/login.html", {"title": "Logout", "message": "Logged Out"}
    )
