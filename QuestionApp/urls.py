from django.urls import re_path as url
from UserApp import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenVerifyView,
    TokenRefreshView,
)

urlpatterns = [

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)