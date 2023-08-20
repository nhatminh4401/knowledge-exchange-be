from unicodedata import name
from django.urls import re_path as url
from user.views import userApi, create_user


urlpatterns = [
    url(r'^user/$', userApi.as_view()),
    url('create_user/', create_user),
]
