from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favorites/", include("Favorites.urls")),
    path("recommendations/", include("Recommendations.urls")),
    path("suggest/", include("Suggest.urls")),
    path("", include("Docs.urls"))
]