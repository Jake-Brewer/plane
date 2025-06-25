"""
Local Analytics API URLs
Secure routing for local analytics dashboard with exception handling
"""

from django.urls import path
from plane.api.views import local_analytics

urlpatterns = [
    # Dashboard endpoints
    path('dashboard/', local_analytics.analytics_dashboard, 
         name='analytics_dashboard'),
    path('health/', local_analytics.health_check, name='analytics_health'),
    
    # Data retrieval endpoints
    path('events/', local_analytics.user_events, name='user_events'),
    path('errors/summary/', local_analytics.error_summary, 
         name='error_summary'),
    
    # Data logging endpoints (POST)
    path('events/', local_analytics.log_event, name='log_event'),
    path('errors/', local_analytics.log_error, name='log_error'),
    path('pageviews/', local_analytics.log_page_view, name='log_page_view'),
    path('session-recordings/', local_analytics.log_session_recording, 
         name='log_session_recording'),
    path('metrics/', local_analytics.log_performance_metric, 
         name='log_performance_metric'),
    path('telemetry/', local_analytics.log_plane_telemetry, 
         name='log_plane_telemetry'),
] 