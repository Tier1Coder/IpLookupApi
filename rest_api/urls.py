"""
URL routing for rest_api project.
"""

from django.urls import path
from .views import get_ip_tags_json, get_ip_tags_report

urlpatterns = [
    path('ip-tags/<str:ip>/', get_ip_tags_json, name='ip_tags_json'),
    path('ip-tags-report/<str:ip>/', get_ip_tags_report, name='ip_tags_report'),
]
