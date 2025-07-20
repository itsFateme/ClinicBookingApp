# appointments/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AppointmentViewSet
from .reports_views import AppointmentReportView 
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls