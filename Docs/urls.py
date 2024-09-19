from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("favorites_API/", views.docs_view),
    path("examples/<slug:url_key>/", views.example)
]
