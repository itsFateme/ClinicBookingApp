# services/models.py
from django.db import models
from clinics.models import Clinic
from doctors.models import Doctor

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='services')
    doctors = models.ManyToManyField(Doctor, related_name='services_offered', blank=True)

    def __str__(self):
        return self.name