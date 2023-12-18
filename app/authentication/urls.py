from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CustomUserRegistrationViewSet

urlpatterns = [
    path(
        "register/",
        CustomUserRegistrationViewSet.as_view({"post": "create"}),
        name="register",
    ),
    path(
        "verification_register/",
        CustomUserRegistrationViewSet.as_view({"post": "verification_register"}),
        name="verify_register",
    ),
    path(
        "register/verify_email/",
        CustomUserRegistrationViewSet.as_view({"post": "verify_email"}),
        name="verify_email",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
