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


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number", "address", "image"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email != email and User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not re.match(r"^\d+$", phone):
            raise ValidationError("Phone number can contain only digits.")
        if phone != phone and User.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is already in use.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})



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

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        service = cleaned_data.get("service")
        pet = cleaned_data.get("pet")

        if service is None:
            errors.append("You must select a valid service.")
        if pet is None:
            errors.append("You must select a valid pet.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "breed", "age", "medical_notes", "image"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        self.fields["breed"] = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

        self.fields["age"] = forms.IntegerField(
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

        self.fields["medical_notes"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional information here...'
            })
        )

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        name = cleaned_data.get("name")
        breed = cleaned_data.get("breed")
        age = cleaned_data.get("age")

        if not name:
            errors.append("Pet name cannot be empty.")
        if not breed:
            errors.append("Breed cannot be empty.")
        if age is None:
            errors.append("Age cannot be empty.")
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors.append("Pet name can only contain letters and white spaces.")
        if breed and not re.match(r'^[A-Za-z\s]+$', breed):
            errors.append("Breed can only contain letters and white spaces.")
        if age and age <= 0:
            errors.append("Age must be a positive number.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data


class EditPetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "breed", "age", "medical_notes", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'edit_pet_name'})
        )

        self.fields["breed"] = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'edit_pet_breed'}),
        )

        self.fields["age"] = forms.IntegerField(
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'edit_pet_age'})
        )

        self.fields["medical_notes"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'edit_medical_notes',
                'placeholder': 'Enter additional information here...'
            })
        )

        self.fields['image'].widget.attrs.update({'class': 'form-control', 'id': 'edit_pet_image'})

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        name = cleaned_data.get("name")
        breed = cleaned_data.get("breed")
        age = cleaned_data.get("age")

        if not name:
            errors.append("Pet name cannot be empty.")
        if not breed:
            errors.append("Breed cannot be empty.")
        if age is None:
            errors.append("Age cannot be empty.")
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors.append("Pet name can only contain letters and white spaces.")
        if breed and not re.match(r'^[A-Za-z\s]+$', breed):
            errors.append("Breed can only contain letters and white spaces.")
        if age and age <= 0:
            errors.append("Age must be a positive number.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data
