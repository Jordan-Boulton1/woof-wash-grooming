from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegistrationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "grooming_service/register.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, "grooming_service/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, "grooming_service/home.html")

def about(request):
    return render(request, "grooming_service/about.html")

def contact(request):
    return render(request, "grooming_service/contact.html")

def services(request):
    return render(request, "grooming_service/services.html")