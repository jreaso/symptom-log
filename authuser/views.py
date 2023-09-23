from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            # return HttpResponseRedirect(reverse("dashboard"))
            return HttpResponse("Logged In")
        # Otherwise, return login page again with new context
        else:
            return render(
                request,
                "authuser/login.html",
                {"title": "Login", "message": "Invalid Credentials"},
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
