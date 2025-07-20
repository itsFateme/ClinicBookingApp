# appointments/reports_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
import datetime

from .models import Appointment

class AppointmentReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if not (user.is_superuser or user.role == 'system_admin' or user.role == 'clinic_admin'):
            return Response({"detail": "You do not have permission to access this report."}, status=status.HTTP_403_FORBIDDEN)

        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        queryset = Appointment.objects.all()

        if user.role == 'clinic_admin' and hasattr(user, 'managed_clinic'):
            queryset = queryset.filter(clinic=user.managed_clinic)

        try:
            if start_date_str:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            if end_date_str:
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                end_date = end_date + datetime.timedelta(days=1)
                queryset = queryset.filter(date__lt=end_date)
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        total_appointments = queryset.count()

        appointments_by_status = queryset.values('status').annotate(count=Count('id'))

        appointments_by_doctor = queryset.values(
            'doctor__user__first_name',
            'doctor__user__last_name',
            'doctor__specialty'
        ).annotate(count=Count('id'))


        return Response({
            "total_appointments": total_appointments,
            "appointments_by_status": list(appointments_by_status),
            "appointments_by_doctor": list(appointments_by_doctor),
        }, status=status.HTTP_200_OK)