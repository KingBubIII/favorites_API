from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("top/<int:amount>/", views.top),
    path("top/<int:amount>/<str:category>/", views.top),
    path("latest/", views.latest),
    path("latest/<str:category>/", views.latest),
    path("random/", views.random),
    path("random/<str:category>/", views.random),
    path("search/<str:str_match>/", views.search),
    path("search/<str:str_match>/<str:category>/", views.search),
]
