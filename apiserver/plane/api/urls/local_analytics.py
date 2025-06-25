"""
URL routing for Local Analytics API
Routes all analytics endpoints that replace external service calls
"""

from django.urls import path
from plane.api.views.local_analytics import (
    analytics_dashboard,
    user_events,
    log_event,
    log_error,
    log_page_view,
    log_session_recording,
    log_performance_metric,
    log_plane_telemetry,
    health_check,
)

urlpatterns = [
    # Dashboard endpoint - main analytics overview
    path('dashboard/', analytics_dashboard, name='local_analytics_dashboard'),
    
    # Data retrieval endpoints
    path('events/', user_events, name='local_analytics_events'),
    path('health/', health_check, name='local_analytics_health'),
    
    # Data ingestion endpoints (replacements for external services)
    path('events/log/', log_event, name='log_user_event'),
    path('errors/', log_error, name='log_error'),
    path('page-views/', log_page_view, name='log_page_view'),
    path('sessions/', log_session_recording, name='log_session'),
    path('metrics/', log_performance_metric, name='log_metric'),
    path('telemetry/', log_plane_telemetry, name='log_telemetry'),
] 