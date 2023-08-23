from django.urls import path
from . import views

urlpatterns = [
	path("questions", views.QuestionAPI.as_view()),
    path("categories", views.CategoryAPI.as_view()),
    path("tags", views.TagAPI.as_view()),
    path("links", views.ReferenceLinkAPI.as_view()),
    path("images", views.ImageAPI.as_view()),
]