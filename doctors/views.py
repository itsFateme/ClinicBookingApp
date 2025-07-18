# doctors/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny 
from .models import Doctor, DoctorAvailability
from .serializers import DoctorSerializer, DoctorAvailabilitySerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']: 
            permission_classes = [AllowAny]
        else: 
            permission_classes = [IsAuthenticated, IsAdminUser] 
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'system_admin' or user.is_superuser:
                return Doctor.objects.all()
            elif user.role == 'clinic_admin' and hasattr(user, 'managed_clinic'):
                return Doctor.objects.filter(clinic=user.managed_clinic)
            elif user.role == 'doctor' and hasattr(user, 'doctor_profile'):
                return Doctor.objects.filter(user=user) 
        return Doctor.objects.all() 

class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']: 
            permission_classes = [AllowAny] 
        else: 
            permission_classes = [IsAuthenticated, IsAdminUser] 
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'system_admin' or user.is_superuser:
                return DoctorAvailability.objects.all()
            elif user.role == 'clinic_admin' and hasattr(user, 'managed_clinic'):
                return DoctorAvailability.objects.filter(doctor__clinic=user.managed_clinic)
            elif user.role == 'doctor' and hasattr(user, 'doctor_profile'):
                return DoctorAvailability.objects.filter(doctor=user.doctor_profile)
        return DoctorAvailability.objects.all() 