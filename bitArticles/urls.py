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

# urls for debugging tools
if settings.DEBUG and settings.IS_SILK_ENABLED:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
