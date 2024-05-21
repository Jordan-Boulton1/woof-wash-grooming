from django import forms
from django.core.exceptions import ValidationError
from django_flatpickr.widgets import DateTimePickerInput
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


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "pet", "start_date_time", "description"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["start_date_time"].widget = DateTimePickerInput(
            options=FlatpickrOptions(
                altFormat="d-m-Y H:i",
            )
        )
        self.fields["start_date_time"].widget.attrs.update({'class': 'form-control', 'required': 'true'})

        self.fields["service"] = forms.ModelChoiceField(
            queryset=Service.objects.all(),
            required=True,
            empty_label="Select a service"
        )
        self.fields["service"].widget.attrs.update({'class': 'form-control'})

        self.fields["pet"] = forms.ModelChoiceField(
            queryset=Pet.objects.none(),
            required=True,
            empty_label="Select a pet"
        )
        self.fields["description"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional information here...'
            })
        )
        self.fields["pet"].widget.attrs.update({'class': 'form-control'})
        if user:
            self.fields["pet"].queryset = Pet.objects.filter(user=user)





class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["pet_name", "breed", "age", "medical_notes"]
