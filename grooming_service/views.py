from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from .forms import *
from .models import Service

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

def get_services(request):
    services = Service.objects.all()
    return render(request, "grooming_service/services.html", {'services': services})

def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
    else:
        form = AppointmentForm()
    
    return render(request, "grooming_service/appointment.html", {"form": form})

def get_available_times(request, selected_date):
    date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    available_times = []
    for dt in Appointment.objects.filter(status=0, start_date_time__date=date).values_list("start_date_time", flat=True):
        available_times.append(dt.time().isoformat())
    return JsonResponse(available_times, safe=False)