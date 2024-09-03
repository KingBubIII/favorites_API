from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("top/<int:amount>/", views.top_all),
    path("top/<int:amount>/<str:category>/", views.top_in_category),
    path("latest/", views.latest),
    path("latest/<str:category>/", views.latest_by_category),
]
