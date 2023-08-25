from django.urls import path
from . import views

urlpatterns = [
    path("answers", views.AnswerAPI.as_view()),
    path("links", views.ReferenceLinkAPI.as_view()),
    path("images", views.ImageAPI.as_view()),
]
