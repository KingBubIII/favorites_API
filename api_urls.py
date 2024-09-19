from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favorites/", include("Favorites.urls"), name='favorites'),
    path("recommendations/", include("Recommendations.urls"), name='recommendations'),
    path("suggest/", include("Suggest.urls"), name='suggest'),
]