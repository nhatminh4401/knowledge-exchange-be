from unicodedata import name
from django.urls import re_path as url
from user.views import userApi, RankingApi


urlpatterns = [
    url(r'^user/$', userApi.as_view()),
    url('user/ranking/', RankingApi.as_view(), name='ranking-api'),
]
