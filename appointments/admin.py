from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'date', 'start_time', 'status', 'booking_timestamp')
    list_filter = ('status', 'date', 'doctor__specialty', 'clinic')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    raw_id_fields = ('patient', 'doctor', 'clinic')
    date_hierarchy = 'date' 