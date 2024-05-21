from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from grooming_service.forms import *
from .models import Service


# Register view
def register(request):
    # Handle POST request
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


# User login view
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


# User logout view
def user_logout(request):
    logout(request)
    return redirect('home')


# Home view
def home(request):
    return render(request, "grooming_service/home.html")


# About view
def about(request):
    return render(request, "grooming_service/about.html")


# Get services view
def get_services(request):
    services = Service.objects.all()
    return render(request, "grooming_service/services.html", {'services': services})


# Book appointment view
@login_required(login_url='login')
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            start_date_time = form.cleaned_data["start_date_time"]
            description = form.cleaned_data["description"]
            pet = form.cleaned_data["pet"]
            service = form.cleaned_data["service"]
            try:
                check_appointment = Appointment.objects.get(start_date_time=start_date_time, status=1)
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
        form = AppointmentForm(user=request.user)
    return render(request, "grooming_service/appointment.html", {"form": form})


# Manage profile view
@login_required(login_url='login')
def manage_profile(request):
    appointmentForm = AppointmentForm(request.POST or None, user=request.user)
    petForm = PetForm(request.POST or None)
    if request.method == "POST":
        if len(appointmentForm.changed_data) != 0:
            __handle_edit_appointment_form(request, appointmentForm)
        if len(petForm.changed_data) != 0:
            __handle_pet_add_form(request, petForm)
    appointments = Appointment.objects.filter(user=request.user).order_by('start_date_time')
    pets = Pet.objects.filter(user=request.user).order_by('pet_name')
    return render(request, "grooming_service/profile.html", {'appointmentForm': appointmentForm,
                                                             'appointments': appointments,
                                                             'pets': pets,
                                                             'petForm': petForm})


# Handle edit appointment form
def __handle_edit_appointment_form(request, appointmentForm):
    appointment_id = request.POST.get("appointment_id")
    start_date_time = request.POST.get("start_date_time")
    description = appointmentForm.data["description"]
    pet = appointmentForm.data["pet"]
    service = appointmentForm.data["service"]
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        request_date_time_obj = datetime.strptime(start_date_time, "%d-%m-%Y %H:%M")
        formatted_date_time = request_date_time_obj.strftime('%Y-%m-%d %H:%M')
        if appointment.start_date_time.strftime('%Y-%m-%d %H:%M') != formatted_date_time:
            if Appointment.objects.filter(start_date_time=formatted_date_time, status=1).exists():
                messages.error(request, "The selected appointment slot is no longer available")
                return redirect("profile")
            else:
                appointment.start_date_time = request_date_time_obj
        appointment.pet_id = pet
        appointment.service_id = service
        appointment.description = description
        appointment.save()
        messages.success(request, "Your appointment has been successfully updated")
        return redirect("profile")
    except Appointment.DoesNotExist:
        messages.error(request, "The requested appointment does not exist")


# Handle adding pet form
def __handle_pet_add_form(request, petForm):
    if petForm.is_valid():
        pet_name = petForm.cleaned_data["pet_name"]
        breed = petForm.cleaned_data["breed"]
        age = petForm.cleaned_data["age"]
        medical_notes = petForm.cleaned_data["medical_notes"]
        pet = Pet()
        pet.pet_name = pet_name
        pet.breed = breed
        pet.age = age
        pet.medical_notes = medical_notes
        pet.user = request.user
        pet.save()
        return redirect("profile")
    else:
        messages.error(request, "Invalid pet data")


# Cancel appointment view
@login_required(login_url='login')
def cancel_appointment(request, cancel_appointment_id):
    try:
        appointment = get_object_or_404(Appointment, id=cancel_appointment_id)
        if appointment.user == request.user:
            appointment.delete()
            messages.success(request, "Your appointment has been successfully cancelled.")
            return redirect("profile")
        else:
            messages.error(request, "You do not have permission to cancel this appointment.")
    except Appointment.DoesNotExist:
        messages.error(request, "The requested appointment does not exist.")
    return redirect("profile")


@login_required(login_url='login')
def delete_pet(request, delete_pet_id):
    try:
        pet = get_object_or_404(Pet, id=delete_pet_id)
        if pet.user == request.user:
            pet.delete()
            messages.success(request, "Your pet has been successfully deleted.")
            return redirect("profile")
        else:
            messages.error(request, "You do not have permission to delete this pet.")
    except Pet.DoesNotExist:
        messages.error(request, "The requested pet does not exist.")
    return redirect("profile")


# Get appointment by ID view
@login_required(login_url='login')
def get_appointment_by_id(request, appointment_id):
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_data = {
                "id": appointment.id,
                "start_date_time": appointment.start_date_time.strftime('%d-%m-%Y %H:%M'),
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
