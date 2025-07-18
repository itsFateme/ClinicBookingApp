from django.db import models

# Create your models here.
# doctors/models.py

from users.models import User
from clinics.models import Clinic 

class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile', limit_choices_to={'role': 'doctor'})
    specialty = models.CharField(max_length=100)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')
    bio = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(default=0)

    def __str__(self):

        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialty})"

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.IntegerField(default=15)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')

    def __str__(self):
        return f"{self.doctor} on {self.date} from {self.start_time} to {self.end_time}"