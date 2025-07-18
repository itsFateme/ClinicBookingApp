from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Clinic

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'clinic_admin')
    search_fields = ('name', 'address')