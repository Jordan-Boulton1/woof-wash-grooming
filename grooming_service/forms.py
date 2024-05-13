from django import forms
from django.core.exceptions import ValidationError
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from django.utils import timezone
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
    start_date = forms.DateField(required=True, widget=DatePickerInput())
    start_time = forms.ChoiceField(required=True, widget=forms.Select())
    pet = forms.ModelChoiceField(queryset=Pet.objects.all(), required=True, widget=forms.Select(), initial="")
    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=True, widget=forms.Select(), initial="")
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'placeholder': 'Additional information...'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        available_dates = [
            dt.date().isoformat()
            for dt in
            Appointment.objects.filter(status=0, start_date_time__gte=timezone.now()).values_list("start_date_time",
                                                                                                  flat=True)
        ]

        self.fields["start_date"].widget = DatePickerInput(
            options=FlatpickrOptions(
                enable=list(set(available_dates)),
                altFormat="d-m-Y",
            )
        )

        if user:
            self.fields["pet"].queryset = Pet.objects.filter(user=user)
