from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("services.core.urls")),
    path("admin/", admin.site.urls),
]
