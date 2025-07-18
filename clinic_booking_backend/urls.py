# clinic_booking_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/clinics/', include('clinics.urls')),
    path('api/', include('doctors.urls')),
    path('api/', include('services.urls')),
    path('api/', include('appointments.urls')),
]