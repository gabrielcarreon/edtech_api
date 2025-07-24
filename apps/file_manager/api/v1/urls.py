from django.urls import path
from . import views

urlpatterns = [
    path("", views.FileManager.as_view())
]
