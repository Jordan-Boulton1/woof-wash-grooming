from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField()
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100)

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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'woof_wash_grooming"."Pet'

class Appointment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    status = models.IntegerField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()

    class Meta:
        db_table = 'woof_wash_grooming"."Appointment'