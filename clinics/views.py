# clinics/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from .models import Clinic
from .serializers import ClinicSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'system_admin' or user.is_superuser:
                return Clinic.objects.all()
            elif user.role == 'clinic_admin':
                return Clinic.objects.filter(clinic_admin=user)
        return Clinic.objects.none()