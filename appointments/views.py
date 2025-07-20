# appointments/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Appointment
from .serializers import AppointmentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated] 

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'system_admin' or user.is_superuser:
                return Appointment.objects.all()
            elif user.role == 'clinic_admin' and hasattr(user, 'managed_clinic'):
                return Appointment.objects.filter(clinic=user.managed_clinic)
            elif user.role == 'doctor' and hasattr(user, 'doctor_profile'):
                return Appointment.objects.filter(doctor=user.doctor_profile)
            elif user.role == 'patient':
                return Appointment.objects.filter(patient=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['confirmed', 'cancelled', 'completed']:
            return Response({"status": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if user.is_superuser or user.role == 'system_admin':
            pass
        elif user.role == 'doctor' and hasattr(user, 'doctor_profile') and user.doctor_profile == appointment.doctor:
            pass
        elif user.role == 'clinic_admin' and hasattr(user, 'managed_clinic') and user.managed_clinic == appointment.clinic:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        appointment.status = new_status
        appointment.save()
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)