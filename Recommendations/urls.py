from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("latest/", views.latest),
    path("latest/<str:category>/", views.latest_by_category),
    path("random/", views.random_recommendation),
    path("random/<str:category>/", views.random_recommendation_from_category),
    path("search/<str:str_match>/", views.search_recommendation),
    path("search/<str:str_match>/<str:category>/", views.search_recommendation_in_category),
]
