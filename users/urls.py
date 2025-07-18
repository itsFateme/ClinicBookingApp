# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, MyTokenObtainPairView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]