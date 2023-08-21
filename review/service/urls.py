from django.urls import path
from . import views


urlpatterns = [
    path("review-question", views.ReviewQuestionAPI.as_view()),
    path("review-answer", views.ReviewAnswerAPI.as_view()),
    path("review", views.ReviewAPI.as_view()),
]
