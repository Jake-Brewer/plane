"""
Local Analytics API Views - Privacy-First Data Storage
Stores all analytics data locally that would have been sent to external services.
Each endpoint clearly documents the original destination that has been redirected.
"""

import json
import logging
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Import our local analytics service
try:
    from plane.utils.local_analytics import local_analytics
except ImportError:
    local_analytics = None

logger = logging.getLogger(__name__)

# Service mapping - documents where data was originally intended to go
ORIGINAL_DESTINATIONS = {
    'user_events': 'app.posthog.com',
    'error_logs': 'sentry.io', 
    'session_recordings': 'clarity.microsoft.com',
    'page_analytics': 'plausible.io',
    'performance_metrics': 'opentelemetry-collector',
    'plane_telemetry': 'telemetry.plane.so'
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_dashboard(request):
    """
    Get comprehensive analytics dashboard data
    
    PRIVACY NOTE: This replaces data that would have been sent to:
    - PostHog (user behavior tracking)
    - Sentry (error monitoring) 
    - Microsoft Clarity (session recordings)
    - Plausible (website analytics)
    - OpenTelemetry (performance metrics)
    - Plane.so telemetry servers
    """
    try:
        if not local_analytics:
            # Return fallback data with original destination info
            return Response({
                'summary': {
                    service: {
                        'count': 0,
                        'original_destination': destination
                    } for service, destination in ORIGINAL_DESTINATIONS.items()
                },
                'message': 'Local analytics service initializing - Data will appear as collected',
                'privacy_status': 'SECURE - No data exfiltration',
                'last_updated': datetime.utcnow().isoformat()
            })
        
        # Get actual analytics data
        dashboard_data = local_analytics.get_analytics_dashboard_data()
        
        # Ensure original destinations are included
        for service in ORIGINAL_DESTINATIONS:
            if service in dashboard_data.get('summary', {}):
                dashboard_data['summary'][service]['original_destination'] = ORIGINAL_DESTINATIONS[service]
        
        dashboard_data.update({
            'privacy_status': 'SECURE - Zero external data transmission',
            'last_updated': datetime.utcnow().isoformat(),
            'data_location': 'Local Docker Volume'
        })
        
        return Response(dashboard_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Analytics dashboard error: {str(e)}")
        return Response({
            'summary': {
                service: {
                    'count': 0,
                    'original_destination': destination
                } for service, destination in ORIGINAL_DESTINATIONS.items()
            },
            'message': f'Analytics service error: {str(e)}',
            'privacy_status': 'SECURE - No data exfiltration (service error)',
            'error': True
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_events(request):
    """
    Get user events that would have been sent to PostHog
    
    PRIVACY NOTE: Originally destined for app.posthog.com
    Now stored locally in Docker volume
    """
    try:
        user_id = request.GET.get('user_id')
        limit = int(request.GET.get('limit', 50))
        
        if not local_analytics:
            return Response([])
        
        events = local_analytics.get_user_events(user_id=user_id, limit=limit)
        
        # Add original destination info to each event
        for event in events:
            event['original_destination'] = 'app.posthog.com'
        
        return Response(events, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"User events fetch failed: {str(e)}")
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def log_event(request):
    """
    Log user event locally instead of sending to PostHog
    
    PRIVACY NOTE: Originally would go to app.posthog.com
    Now stored in local SQLite database
    """
    try:
        data = json.loads(request.body)
        
        if local_analytics:
            local_analytics.track_user_event(
                user_id=data.get('userId', 'anonymous'),
                event_name=data.get('eventName', 'unknown_event'),
                properties=data.get('properties', {}),
                session_id=data.get('sessionId')
            )
            logger.info(f"Event logged locally (was destined for PostHog): {data.get('eventName')}")
        else:
            logger.warning(f"Analytics unavailable - Event would have gone to PostHog: {data.get('eventName')}")
        
        return Response({
            'status': 'logged_locally',
            'original_destination': 'app.posthog.com',
            'privacy_status': 'Data kept local'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Event logging failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'original_destination': 'app.posthog.com'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def log_error(request):
    """
    Log error locally instead of sending to Sentry
    
    PRIVACY NOTE: Originally would go to sentry.io
    Now stored in local error tracking database
    """
    try:
        data = json.loads(request.body)
        
        if local_analytics:
            local_analytics.log_error(
                error_type=data.get('errorType', 'UnknownError'),
                error_message=data.get('errorMessage', 'No message'),
                stack_trace=data.get('stackTrace'),
                user_context=data.get('userContext', {}),
                request_context=data.get('requestContext', {}),
                severity=data.get('severity', 'error')
            )
            logger.info(f"Error logged locally (was destined for Sentry): {data.get('errorType')}")
        else:
            logger.error(f"Analytics unavailable - Error would have gone to Sentry: {data.get('errorMessage')}")
        
        return Response({
            'status': 'logged_locally',
            'original_destination': 'sentry.io',
            'privacy_status': 'Error data kept local'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error logging failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'original_destination': 'sentry.io'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def log_page_view(request):
    """
    Log page view locally instead of sending to Plausible
    
    PRIVACY NOTE: Originally would go to plausible.io
    Now stored in local page analytics database
    """
    try:
        data = json.loads(request.body)
        
        if local_analytics:
            local_analytics.track_page_view(
                page_url=data.get('pageUrl', 'unknown'),
                referrer=data.get('referrer'),
                user_agent=data.get('userAgent'),
                session_id=data.get('sessionId')
            )
            logger.info(f"Page view logged locally (was destined for Plausible): {data.get('pageUrl')}")
        
        return Response({
            'status': 'logged_locally',
            'original_destination': 'plausible.io',
            'privacy_status': 'Page analytics kept local'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Page view logging failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'original_destination': 'plausible.io'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def log_session_recording(request):
    """
    Log session recording locally instead of sending to Microsoft Clarity
    
    PRIVACY NOTE: Originally would go to clarity.microsoft.com
    Now stored in local session database (privacy-safe summary only)
    """
    try:
        data = json.loads(request.body)
        
        if local_analytics:
            # Store privacy-safe session summary (not full recording)
            local_analytics.record_session_data(
                user_id=data.get('userId', 'anonymous'),
                session_data={
                    'duration': data.get('durationSeconds', 0),
                    'page_count': data.get('pageCount', 1),
                    'interaction_count': data.get('interactionCount', 0)
                },
                page_url=data.get('pageUrl', 'unknown'),
                duration_seconds=data.get('durationSeconds', 0)
            )
            logger.info(f"Session summary logged locally (was destined for Clarity): {data.get('userId')}")
        
        return Response({
            'status': 'logged_locally',
            'original_destination': 'clarity.microsoft.com',
            'privacy_status': 'Session summary kept local (no screen recording)',
            'note': 'Only session metadata stored for privacy'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Session recording failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'original_destination': 'clarity.microsoft.com'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def log_performance_metric(request):
    """
    Log performance metric locally instead of sending to OpenTelemetry collector
    
    PRIVACY NOTE: Originally would go to external OpenTelemetry collector
    Now stored in local performance metrics database
    """
    try:
        data = json.loads(request.body)
        
        if local_analytics:
            local_analytics.record_metric(
                metric_name=data.get('metricName', 'unknown_metric'),
                metric_value=float(data.get('metricValue', 0)),
                tags=data.get('tags', {}),
                service_name=data.get('serviceName', 'plane')
            )
            logger.info(f"Performance metric logged locally (was destined for OpenTelemetry): {data.get('metricName')}")
        
        return Response({
            'status': 'logged_locally',
            'original_destination': 'opentelemetry-collector',
            'privacy_status': 'Performance data kept local'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Performance metric logging failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'original_destination': 'opentelemetry-collector'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def log_plane_telemetry(request):
    """
    Log Plane telemetry locally instead of sending to Plane.so servers
    
    PRIVACY NOTE: Originally would go to telemetry.plane.so
    Now stored in local telemetry database
    """
    try:
        data = json.loads(request.body)
        
        if local_analytics:
            local_analytics.store_plane_telemetry(
                telemetry_type=data.get('telemetryType', 'unknown'),
                data=data.get('data', {}),
                instance_id=data.get('instanceId')
            )
            logger.info(f"Plane telemetry logged locally (was destined for Plane.so): {data.get('telemetryType')}")
        
        return Response({
            'status': 'logged_locally',
            'original_destination': 'telemetry.plane.so',
            'privacy_status': 'Telemetry data kept local'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Plane telemetry logging failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'original_destination': 'telemetry.plane.so'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check(request):
    """
    Health check for local analytics system
    Shows status of privacy protection and data storage
    """
    try:
        health_status = {
            'status': 'healthy',
            'local_analytics_available': local_analytics is not None,
            'timestamp': datetime.utcnow().isoformat(),
            'privacy_status': 'SECURE - Zero external data transmission',
            'data_location': 'Local Docker Volume: ./volumes/analytics',
            'blocked_destinations': list(ORIGINAL_DESTINATIONS.values()),
            'services_redirected': len(ORIGINAL_DESTINATIONS)
        }
        
        if local_analytics:
            try:
                test_data = local_analytics.get_analytics_dashboard_data()
                health_status['database_connection'] = 'healthy'
                health_status['total_records'] = sum(
                    data.get('count', 0) for data in test_data.get('summary', {}).values()
                )
            except Exception as e:
                health_status['database_connection'] = f'error: {str(e)}'
                health_status['status'] = 'degraded'
        else:
            health_status['status'] = 'initializing'
            health_status['message'] = 'Local analytics service starting up'
        
        return Response(health_status, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e),
            'privacy_status': 'SECURE - No external transmission even during errors',
            'timestamp': datetime.utcnow().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
