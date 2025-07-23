from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuizzesListCreate.as_view(), name="quizzes-list-create"),
]
