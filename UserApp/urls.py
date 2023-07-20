from django.urls import re_path as url
from UserApp import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenVerifyView,
    TokenRefreshView,
)

urlpatterns = [
    url(r'^user/$', views.userApi),
    url(r'^user/([0-9]+)$', views.userApi),

    url(r'^savefile', views.SaveFile),
    url("signup/", views.SignUpView.as_view(), name="signup"),
    url("login/", views.LoginView.as_view(), name="login"),
    url("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    url("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    url("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)