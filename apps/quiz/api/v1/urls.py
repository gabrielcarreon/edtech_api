from django.urls import path
from . import views

urlpatterns = [
    path("", views.QuizzesCreate.as_view()),
    path("<int:id>/", views.QuizShow.as_view())
]
