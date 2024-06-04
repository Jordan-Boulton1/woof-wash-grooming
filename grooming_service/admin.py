from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.hashers import make_password
from .models import *


# Register the Service model with the admin interface
@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):
    # Enable Summernote editor for 'description' and 'short_description' fields
    summernote_fields = ('description', 'short_description')
    list_display = ['name', 'vary_price1', 'vary_price2']


# Define an admin class for Appointment model
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'pet', 'status', 'start_date_time']
    # Excluding as admins should not be editing or putting description on requested appointments # noqa
    exclude = ['description']


# Register the Appointment model with the custom AppointmentAdmin class
admin.site.register(Appointment, AppointmentAdmin)


# Define an admin class for Pet model
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'age', 'user', 'medical_notes']


# Register the Appointment model with the custom AppointmentAdmin class
admin.site.register(Pet, PetAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number',
                    'address']

    # Prevent passwords to be saves as
    # raw text when updated through admin
    # panel
    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            # Hash the password before saving
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


# Register the User model with the admin interface
admin.site.register(User, UserAdmin)
