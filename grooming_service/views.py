from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from grooming_service.forms import *
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
        if form.is_valid():
            start_date_time = form.cleaned_data["start_date_time"]
            description = form.cleaned_data["description"]
            pet = form.cleaned_data["pet"]
            service = form.cleaned_data["service"]

            try:
                check_appointment = Appointment.objects.get(start_date_time=start_date_time, status=1)
                if check_appointment:
                    messages.error(request, "The selected appointment is no longer available")
                    return redirect("appointment")
            except Appointment.DoesNotExist:
                appointment = Appointment(user=request.user,
                                          pet=pet,
                                          status=1,
                                          service=service,
                                          start_date_time=start_date_time,
                                          description=description)
                appointment.save()
                messages.success(request, "Your appointment has been booked.")
                return redirect("profile")

        else:
            messages.error(request, "There was an error booking this appointment.")
    else:
        form = AppointmentForm()

    return render(request, "grooming_service/appointment.html", {"form": form})


@login_required(login_url='login')
def manage_appointments(request):
    form = PartialAppointmentForm(request.POST or None)

    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        start_date = request.POST.get("start_date")
        description = form.data["description"]
        pet = form.data["pet"]
        service = form.data["service"]


        try:
            start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
            start_date_obj = datetime.strptime(start_date, "%d-%m-%Y").date()
            start_date_time = datetime.combine(start_date_obj, start_time_obj)
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.start_date_time != start_date_time:
                selected_appointment = Appointment.objects.get(status=0, start_date_time=start_date_time)
                selected_appointment.status = 1
                selected_appointment.save()
                try:
                    previous_appointment = Appointment.objects.get(
                        status=1,
                        start_date_time=appointment.start_date_time,
                        pet_id=None, service_id=None)
                    previous_appointment.status = 0
                    previous_appointment.save()
                except Appointment.DoesNotExist:
                    appointment.start_date_time = start_date_time
                    appointment.pet_id = pet
                    appointment.service_id = service
                    appointment.description = description
                    appointment.save()
            appointment.start_date_time = start_date_time
            appointment.pet_id = pet
            appointment.service_id = service
            appointment.description = description

            appointment.save()

            return redirect("profile")
        except Appointment.DoesNotExist:
            messages.error(request, "The selected appointment is no longer available")

    appointments = Appointment.objects.filter(user=request.user).order_by('start_date_time')
    return render(request, "grooming_service/profile.html", {'form': form, 'appointments': appointments})


@login_required(login_url='login')
def get_available_times(request, selected_date):
    date = datetime.strptime(selected_date, "%d-%m-%Y").date()

    available_times = []
    for dt in Appointment.objects.filter(status=0, start_date_time__date=date).values_list("start_date_time",
                                                                                           flat=True):
        available_times.append(dt.time().isoformat())
    return JsonResponse(available_times, safe=False)


@login_required(login_url='login')
def get_available_dates(request):
    available_dates = []
    for dt in Appointment.objects.filter(status=0, start_date_time__gte=timezone.now()).values_list("start_date_time",
                                                                                                    flat=True):
        available_dates.append(dt.date().isoformat())
    return JsonResponse(available_dates, safe=False)


@login_required(login_url='login')
def get_appointment_by_id(request, appointment_id):
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_data = {
                "id": appointment.id,
                "start_date": appointment.start_date_time.date().strftime('%d-%m-%Y'),
                "start_time": appointment.start_date_time.time(),
                "description": appointment.description,
                "pet": {
                    "name": appointment.pet.pet_name,
                    "id": appointment.pet.id
                },
                "service": {
                    "name": appointment.service.name,
                    "id": appointment.service.id
                }
            }
            return JsonResponse({"appointment": appointment_data})
        except Appointment.DoesNotExist:
            return JsonResponse({"message": "Appointment not found"}, status=404)
    return JsonResponse({"message": "Invalid request"}, status=400)
