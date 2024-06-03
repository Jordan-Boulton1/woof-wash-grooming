from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .validators import Validators
from .custom_user_manager import CustomUserManager
import sys


# Define the custom User model, inheriting from AbstractBaseUser and PermissionsMixin for custom user management # noqa
class User(AbstractBaseUser, PermissionsMixin):
    # User's first name with validation
    first_name = models.CharField(
        max_length=50, validators=[Validators.validate_string_input]
    )
    # User's last name with validation
    last_name = models.CharField(
        max_length=50, validators=[Validators.validate_string_input]
    )
    # Unique email field
    email = models.EmailField(
        max_length=255, unique=True,
        error_messages={"unique": "This email is already in use."}
    )
    # User's password
    password = models.CharField(max_length=100)
    # Unique phone number with validation
    phone_number = models.CharField(
        max_length=30, unique=True,
        error_messages={"unique": "This phone number is already in use."},
        validators=[Validators.validate_phone_number]
    )
    # User's address
    address = models.CharField(max_length=100)
    # User's profile image with a default value
    image = models.ImageField(
        upload_to='images/', default='media/images/go9xwcxemxj7sajmn1zf'
    )
    # Indicates if the user is a staff member
    is_staff = models.BooleanField(default=False)
    # Indicates if the user is active
    is_active = models.BooleanField(default=True)
    # Set the username field to email for authentication
    USERNAME_FIELD = "email"

    objects = CustomUserManager()  # Use the custom user manager

    def __str__(self):
        return self.email  # String representation of the user

    class Meta:
        # Point to the posgres schema for the database table for
        # non-test environments
        if 'test' not in sys.argv:
            db_table = 'woof_wash_grooming"."User'


# Define the Service model
class Service(models.Model):
    # Name of the service
    name = models.CharField(max_length=50)
    # Detailed description of the service
    description = models.TextField()
    # Variable price 1 for the service
    vary_price1 = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    # Variable price 2 for the service
    vary_price2 = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    # Image for the service with a default value
    image = models.ImageField(
        upload_to='images/', default='media/images/rlbpt7uaqhxanu59ro9r'
    )
    # Short description of the service
    short_description = models.TextField(default="")

    def __str__(self):
        # String representation of the service
        return self.name

    class Meta:
        if 'test' not in sys.argv:
            # Point to the posgres schema for the database table
            # for non-test environments
            db_table = 'woof_wash_grooming"."Service'


# Define the Pet model
class Pet(models.Model):
    # Name of the pet
    name = models.CharField(max_length=255)
    # Breed of the pet
    breed = models.CharField(max_length=255)
    # Age of the pet
    age = models.IntegerField()
    # Medical notes about the pet, nullable
    medical_notes = models.TextField(null=True)
    # Reference to the owner user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Image of the pet with a default value
    image = models.ImageField(
        upload_to='images/', default='media/images/tey9seavfcldmybatmmt'
    )

    def __str__(self):
        # String representation of the pet
        return self.name

    class Meta:
        if 'test' not in sys.argv:
            # Point to the posgres schema for the database table for
            # non-test environments
            db_table = 'woof_wash_grooming"."Pet'


# Define status choices for appointments
STATUS = ((1, "booked"), (2, "completed"))


# Define the Appointment model
class Appointment(models.Model):
    # Reference to the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Reference to the service
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    # Reference to the pet
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # Status of the appointment with choices
    status = models.IntegerField(choices=STATUS, default=0)
    # Start date and time of the appointment
    start_date_time = models.DateTimeField()
    # Description of the appointment, nullable
    description = models.TextField(null=True)

    class Meta:
        if 'test' not in sys.argv:
            # Point to the posgres schema for the database table for
            # non-test environments
            db_table = 'woof_wash_grooming"."Appointment'

    def __str__(self):
        return f"{self.pet}"  # String representation of the appointment
