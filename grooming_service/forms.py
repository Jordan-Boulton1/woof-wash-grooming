from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
import re

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "password"]

    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not re.match(r"^\d+$", phone):
            raise ValidationError("Phone number can contain only digits.")
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is already in use.")
        return phone