from django.db import models

# Create your models here.
# clinics/models.py
from users.models import User 
class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    clinic_admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='managed_clinic', limit_choices_to={'role': 'clinic_admin'})

    def __str__(self):
        return self.name