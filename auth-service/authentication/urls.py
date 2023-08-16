from unicodedata import name
from django.urls import re_path as url
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenVerifyView,
    TokenRefreshView,
)

from authentication.views import LoginView, SignUpView

urlpatterns = [
    url("register/", SignUpView.as_view(), name="register"),
    url("login/", LoginView.as_view(), name="login"),
    url("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    url("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    url("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
