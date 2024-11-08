"""
URL configuration for bitArticles project.
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.API_PREFIX, include('api.urls')),
]
