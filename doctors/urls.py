# doctors/urls.py
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DoctorAvailabilityViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'availabilities', DoctorAvailabilityViewSet, basename='doctor-availability')

urlpatterns = router.urls