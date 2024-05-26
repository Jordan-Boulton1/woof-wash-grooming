from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.

@admin.register(Service)
class PostAdmin(SummernoteModelAdmin):

    summernote_fields = ('description', 'short_description')

class AppointmentAdmin(admin.ModelAdmin):
    exclude = ['user', 'pet', 'service']

admin.site.register(User)
admin.site.register(Appointment, AppointmentAdmin)