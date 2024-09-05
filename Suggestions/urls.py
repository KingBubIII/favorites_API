from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("latest/", views.latest),
    path("latest/<str:category>/", views.latest_by_category),
    path("random/", views.random_suggestion),
    path("random/<str:category>/", views.random_suggestion_from_category),
    path("search/<str:str_match>/", views.search_suggestion),
    path("search/<str:str_match>/<str:category>/", views.search_suggestion_in_category),
]
