from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import Validators


from .custom_user_manager import CustomUserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, validators=[Validators.validate_string_input])
    last_name = models.CharField(max_length=50, validators=[Validators.validate_string_input])
    email = models.EmailField(max_length=255, unique=True, error_messages={"unique": "This email is already in use."})
    password = models.CharField()
    phone_number = models.CharField(max_length=30, unique=True, 
                                    error_messages={"unique": "This phone number is already in use."}, 
                                    validators=[Validators.validate_phone_number])
    address = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'woof_wash_grooming"."User'


class Service(models.Model):
    service_name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'woof_wash_grooming"."Service'

class Pet(models.Model):
    pet_name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    medical_notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'woof_wash_grooming"."Pet'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    status = models.IntegerField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()

    class Meta:
        db_table = 'woof_wash_grooming"."Appointment'