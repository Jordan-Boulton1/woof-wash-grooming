from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import User, Service

# Register your models here.

@admin.register(Service)
class PostAdmin(SummernoteModelAdmin):

    summernote_fields = ('description',)


admin.site.register(User)