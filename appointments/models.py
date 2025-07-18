from django.db import models

# Create your models here.
# appointments/models.py
from users.models import User
from doctors.models import Doctor # ایمپورت مدل Doctor
from clinics.models import Clinic # ایمپورت مدل Clinic

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments', limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic_appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    STATUS_CHOICES = (
        ('pending', 'در انتظار تأیید'),
        ('confirmed', 'تأیید شده'),
        ('cancelled', 'لغو شده'),
        ('completed', 'انجام شده'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    booking_timestamp = models.DateTimeField(auto_now_add=True) 

    class Meta:

        unique_together = ('doctor', 'date', 'start_time')
        ordering = ['-date', '-start_time']

    def __str__(self):
        patient_name = f"{self.patient.first_name} {self.patient.last_name}" if self.patient.first_name and self.patient.last_name else self.patient.email
        doctor_name = f"Dr. {self.doctor.user.first_name} {self.doctor.user.last_name}" if self.doctor.user.first_name and self.doctor.user.last_name else self.doctor.user.email
        return f"نوبت {patient_name} با {doctor_name} در {self.date} ساعت {self.start_time}"