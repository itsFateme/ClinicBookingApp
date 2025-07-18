from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor, DoctorAvailability

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'clinic', 'experience_years')
    list_filter = ('specialty', 'clinic')
    search_fields = ('user__first_name', 'user__last_name', 'specialty')

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'slot_duration')
    list_filter = ('date', 'doctor__specialty', 'doctor__clinic')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')
    ordering = ('date', 'start_time')