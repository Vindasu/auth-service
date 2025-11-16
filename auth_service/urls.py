"""
URL configuration for auth_service project.

Main URL routing for the authentication microservice.
"""
from django.contrib import admin
from django.urls import path, include
from authentication.views import health_check

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Authentication API endpoints
    path('auth/', include('authentication.urls')),
    
    # Health check endpoint (for monitoring)
    path('health/', health_check, name='health_check'),
    
    # Root endpoint - API info
    path('', health_check, name='root'),
]
