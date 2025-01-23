from django.urls import path
from . import views

urlpatterns = [path("core/", views.sample_api, name="sample_api"),
               path("", views.health_check, name="health_check")
               ]
