from django.urls import path
from . import views

urlpatterns = [
	path("question/", views.QuestionAPI.as_view()),
    path("categories/", views.CategoryAPI.as_view()),
    path("tags/", views.TagAPI.as_view()),
]