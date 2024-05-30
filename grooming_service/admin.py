from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.

# Register the Service model with the admin interface
@admin.register(Service)
class PostAdmin(SummernoteModelAdmin):
    # Enable Summernote editor for 'description' and 'short_description' fields
    summernote_fields = ('description', 'short_description')


# Define an admin class for Appointment model to exclude certain fields
class AppointmentAdmin(admin.ModelAdmin):
    exclude = ['user', 'pet', 'service']


# Register the User model with the admin interface
admin.site.register(User)

# Register the Appointment model with the custom AppointmentAdmin class
admin.site.register(Appointment, AppointmentAdmin)
