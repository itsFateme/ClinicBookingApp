# clinics/urls.py
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet

router = DefaultRouter()
router.register(r'', ClinicViewSet, basename='clinic')

urlpatterns = router.urls