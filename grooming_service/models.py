from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.templatetags.static import static
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
    image = models.ImageField(upload_to='images/', default='media/images/go9xwcxemxj7sajmn1zf')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'woof_wash_grooming"."User'


class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    vary_price1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    vary_price2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'woof_wash_grooming"."Service'

class Pet(models.Model):
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    medical_notes = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='media/images/tey9seavfcldmybatmmt')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'woof_wash_grooming"."Pet'

STATUS = ((0, "available"), (1, "booked"), (2, "cancelled"))

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    start_date_time = models.DateTimeField()
    description = models.TextField(null=True)

    class Meta:
        db_table = 'woof_wash_grooming"."Appointment'
    
    def __str__(self):
        return f"{self.description}"