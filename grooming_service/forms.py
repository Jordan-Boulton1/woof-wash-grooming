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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'required': 'true'})

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        phone_number = cleaned_data.get("phone_number")
        address = cleaned_data.get("address")

        errors = Validators.append_error_messages_when_field_is_empty(first_name, "First name cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(last_name, "Last name cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(email, "Email cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(password, "Password cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(phone_number, "Phone number cannot be empty",
                                                                      errors)
        errors = Validators.append_error_messages_when_field_is_empty(address, "Address cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(phone_number, r"^\d+$",
                                                                                  "Phone number can contain only digits.",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(email,
                                                                                  r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$',
                                                                                  "Valid email must be provided",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(first_name, r'^[A-Za-z\s]+$',
                                                                                  "First name can only contain letters and white spaces.",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(last_name, r'^[A-Za-z\s]+$',
                                                                                  "Last name can only contain letters and white spaces.",
                                                                                  errors)
        if User.objects.filter(phone_number=phone_number).exists():
            errors.append("This phone number is already in use.")
        if User.objects.filter(email=email).exists():
            errors.append("This email is already in use.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number", "address", "image"]

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        phone_number = cleaned_data.get("phone_number")
        address = cleaned_data.get("address")

        errors = Validators.append_error_messages_when_field_is_empty(first_name, "First name cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(last_name, "Last name cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(email, "Email cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(password, "Password cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(phone_number, "Phone number cannot be empty",
                                                                      errors)
        errors = Validators.append_error_messages_when_field_is_empty(address, "Address cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(phone_number, r"^\d+$",
                                                                                  "Phone number can contain only digits.",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(email,
                                                                                  r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$',
                                                                                  "Valid email must be provided",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(first_name, r'^[A-Za-z\s]+$',
                                                                                  "First name can only contain letters and white spaces.",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(last_name, r'^[A-Za-z\s]+$',
                                                                                  "Last name can only contain letters and white spaces.",
                                                                                  errors)
        if phone_number != phone_number and User.objects.filter(phone_number=phone_number).exists():
            errors.append("This phone number is already in use.")
        if email != email and User.objects.filter(email=email).exists():
            errors.append("This email is already in use.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data

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

        errors = Validators.append_error_messages_when_field_is_empty(name, "Pet name cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(breed, "Breed cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_is_empty(age, "Age cannot be empty", errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(name, r'^[A-Za-z\s]+$',
                                                                                  "Pet name can only contain letters and white spaces.",
                                                                                  errors)
        errors = Validators.append_error_messages_when_field_does_not_match_regex(breed, r'^[A-Za-z\s]+$',
                                                                                  "Breed can only contain letters and white spaces.",
                                                                                  errors)
        if age and age <= 0:
            errors.append("Age must be a positive number.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data
