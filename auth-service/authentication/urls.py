from unicodedata import name
from django.urls import re_path as url
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView, TokenVerifyView,
#     TokenRefreshView,
# )

from authentication.views import LoginView, SignUpView, userApi

urlpatterns = [
    url(r'^user/$', userApi.as_view(), name='userApi'),
    url("register/", SignUpView.as_view(), name="register"),
    url("login/", LoginView.as_view(), name="login"),
]
