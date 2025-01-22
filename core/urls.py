"""
URL routing for core project.
"""

from django.urls import path, include

urlpatterns = [
    path('', include('rest_api.urls')),
]
