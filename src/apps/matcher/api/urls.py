from django.contrib import admin
from django.urls import path, include, register_converter
from .views import MatchMedicalRecordsView

# urlpatterns (url paths mapped to views or other urlpatterns)
urlpatterns = [
    path('', MatchMedicalRecordsView.as_view())
]