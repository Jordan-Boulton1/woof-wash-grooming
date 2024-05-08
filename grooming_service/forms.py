from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget, TimeInput
from django_flatpickr.widgets import DateTimePickerInput, DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from .models import *
import re


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number", "address"]

    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not re.match(r"^\d+$", phone):
            raise ValidationError("Phone number can contain only digits.")
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is already in use.")
        return phone


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AppointmentForm(forms.Form):
    start_date = forms.DateField(
        widget=SelectDateWidget(),
        label="Appointment Date"
    )
    start_time = forms.ChoiceField(choices=[], label="Start Time", required=True)
    pet = forms.ModelChoiceField(queryset=Pet.objects.all(), required=True)
    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=True)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        available_dates = [
          dt.date().isoformat()
            for dt in Appointment.objects.filter(status=0).values_list("start_date_time", flat=True)
        ]

        available_times = [
            dt.time().isoformat()
            for dt in Appointment.objects.filter(status=0).values_list("start_date_time", flat=True)
        ]

        self.fields["start_date"].widget = DatePickerInput(
            options=FlatpickrOptions(
                enable=list(set(available_dates)),
                altFormat="d-m-Y",
            )
        )

        self.fields["start_time"].choices = [(t, t) for t in available_times]

        if user:
            # Filter `pet` based on the user
            self.fields["pet"].queryset = Pet.objects.filter(user=user)
