# Python imports
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Django imports
from django.conf import settings

# Module imports
from plane.db.models.local_analytics import (
    LocalTelemetryData, 
    LocalWorkspaceTelemetry,
    LocalAnalyticsEvent,
    LocalSystemHealth
)

logger = logging.getLogger(__name__)


class LocalTelemetryService:
    """
    Local telemetry service to replace OpenTelemetry data exfiltration to plane.so
    Stores all telemetry data in local database instead of sending externally
    """
    
    def __init__(self):
        self.enabled = True
        self.service_name = os.environ.get("SERVICE_NAME", "plane-ce-api")
        logger.info("LOCAL_TELEMETRY: Initialized local telemetry service")
    
    def start_span(self, span_name: str, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Start a telemetry span (replaces OpenTelemetry span)
        Returns a span context that can be used to end the span
        """
        span_context = {
            'span_name': span_name,
            'start_time': datetime.now(),
            'attributes': attributes or {},
            'trace_id': f"local_{datetime.now().timestamp()}",
            'span_id': f"span_{datetime.now().microsecond}"
        }
        
        logger.debug(f"LOCAL_TELEMETRY: Started span '{span_name}'")
        return span_context
    
    def end_span(self, span_context: Dict[str, Any], additional_attributes: Dict[str, Any] = None):
        """
        End a telemetry span and store data locally
        """
        try:
            end_time = datetime.now()
            duration_ms = int((end_time - span_context['start_time']).total_seconds() * 1000)
            
            # Merge attributes
            all_attributes = span_context['attributes'].copy()
            if additional_attributes:
                all_attributes.update(additional_attributes)
            
            # Extract common fields from attributes
            instance_data = {
                'span_name': span_context['span_name'],
                'trace_id': span_context['trace_id'],
                'span_id': span_context['span_id'],
                'attributes': all_attributes,
                'duration_ms': duration_ms,
                'instance_id': all_attributes.get('instance_id', 'unknown'),
                'instance_name': all_attributes.get('instance_name', ''),
                'current_version': all_attributes.get('current_version', ''),
                'latest_version': all_attributes.get('latest_version', ''),
                'edition': all_attributes.get('edition', ''),
                'domain': all_attributes.get('domain', ''),
                'user_count': all_attributes.get('user_count', 0),
                'workspace_count': all_attributes.get('workspace_count', 0),
                'project_count': all_attributes.get('project_count', 0),
                'issue_count': all_attributes.get('issue_count', 0),
                'module_count': all_attributes.get('module_count', 0),
                'cycle_count': all_attributes.get('cycle_count', 0),
                'page_count': all_attributes.get('page_count', 0),
            }
            
            # Store in local database
            telemetry_record = LocalTelemetryData.objects.create(**instance_data)
            
            # If this is workspace-specific data, create workspace record
            if span_context['span_name'] == 'workspace_details':
                workspace_data = {
                    'telemetry_data': telemetry_record,
                    'workspace_id': all_attributes.get('workspace_id'),
                    'workspace_slug': all_attributes.get('workspace_slug', ''),
                    'project_count': all_attributes.get('project_count', 0),
                    'issue_count': all_attributes.get('issue_count', 0),
                    'module_count': all_attributes.get('module_count', 0),
                    'cycle_count': all_attributes.get('cycle_count', 0),
                    'cycle_issue_count': all_attributes.get('cycle_issue_count', 0),
                    'module_issue_count': all_attributes.get('module_issue_count', 0),
                    'page_count': all_attributes.get('page_count', 0),
                    'member_count': all_attributes.get('member_count', 0),
                }
                LocalWorkspaceTelemetry.objects.create(**workspace_data)
            
            logger.info(f"LOCAL_TELEMETRY: Stored span '{span_context['span_name']}' ({duration_ms}ms)")
            
        except Exception as e:
            logger.error(f"LOCAL_TELEMETRY: Failed to store telemetry data: {str(e)}")
    
    def track_event(self, event_name: str, distinct_id: str, properties: Dict[str, Any] = None):
        """
        Track an analytics event locally (replaces PostHog)
        """
        try:
            event_data = {
                'event_name': event_name,
                'distinct_id': distinct_id,
                'properties': properties or {},
                'user_id': properties.get('user_id') if properties else None,
                'session_id': properties.get('session_id') if properties else None,
                'workspace_id': properties.get('workspace_id') if properties else None,
                'project_id': properties.get('project_id') if properties else None,
                'ip_address': properties.get('ip_address') if properties else None,
                'user_agent': properties.get('user_agent') if properties else None,
                'referrer': properties.get('referrer') if properties else None,
                'country': properties.get('country') if properties else None,
                'city': properties.get('city') if properties else None,
            }
            
            LocalAnalyticsEvent.objects.create(**event_data)
            logger.info(f"LOCAL_TELEMETRY: Tracked event '{event_name}' for {distinct_id}")
            
        except Exception as e:
            logger.error(f"LOCAL_TELEMETRY: Failed to track event: {str(e)}")
    
    def record_system_health(self, component: str, status: str, metrics: Dict[str, Any] = None):
        """
        Record system health metrics locally
        """
        try:
            health_data = {
                'component': component,
                'status': status,
                'metrics': metrics or {},
                'instance_id': os.environ.get('INSTANCE_ID', 'local'),
                'cpu_usage_percent': metrics.get('cpu_usage') if metrics else None,
                'memory_usage_percent': metrics.get('memory_usage') if metrics else None,
                'disk_usage_percent': metrics.get('disk_usage') if metrics else None,
                'response_time_ms': metrics.get('response_time_ms') if metrics else None,
                'db_connections_active': metrics.get('db_connections') if metrics else None,
                'db_query_time_avg_ms': metrics.get('db_query_time') if metrics else None,
                'error_message': metrics.get('error_message') if metrics else None,
                'error_count': metrics.get('error_count', 0) if metrics else 0,
            }
            
            LocalSystemHealth.objects.create(**health_data)
            logger.debug(f"LOCAL_TELEMETRY: Recorded {component} health: {status}")
            
        except Exception as e:
            logger.error(f"LOCAL_TELEMETRY: Failed to record system health: {str(e)}")
    
    def get_telemetry_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Get a summary of telemetry data for the last N days
        """
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        try:
            # Get recent telemetry data
            recent_telemetry = LocalTelemetryData.objects.filter(
                created_at__gte=cutoff_date
            ).order_by('-created_at')
            
            # Get recent events
            recent_events = LocalAnalyticsEvent.objects.filter(
                created_at__gte=cutoff_date
            ).order_by('-created_at')
            
            # Get system health
            recent_health = LocalSystemHealth.objects.filter(
                created_at__gte=cutoff_date
            ).order_by('-created_at')
            
            summary = {
                'period_days': days,
                'telemetry_records': recent_telemetry.count(),
                'analytics_events': recent_events.count(),
                'health_records': recent_health.count(),
                'latest_instance_data': recent_telemetry.first().__dict__ if recent_telemetry.exists() else None,
                'top_events': list(recent_events.values('event_name').distinct()[:10]),
                'system_status': recent_health.first().status if recent_health.exists() else 'unknown'
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"LOCAL_TELEMETRY: Failed to get summary: {str(e)}")
            return {'error': str(e)}


# Global instance
_local_telemetry = None


def get_local_telemetry() -> LocalTelemetryService:
    """Get the global local telemetry service instance"""
    global _local_telemetry
    if _local_telemetry is None:
        _local_telemetry = LocalTelemetryService()
    return _local_telemetry


def init_local_telemetry():
    """Initialize local telemetry (replaces init_tracer)"""
    service = get_local_telemetry()
    logger.info("LOCAL_TELEMETRY: Local telemetry service initialized")
    return service


def shutdown_local_telemetry():
    """Shutdown local telemetry (replaces shutdown_tracer)"""
    global _local_telemetry
    if _local_telemetry:
        logger.info("LOCAL_TELEMETRY: Local telemetry service shutdown")
        _local_telemetry = None


# Context manager for telemetry spans
class LocalTelemetrySpan:
    """Context manager for local telemetry spans"""
    
    def __init__(self, span_name: str, attributes: Dict[str, Any] = None):
        self.span_name = span_name
        self.attributes = attributes or {}
        self.span_context = None
        self.telemetry = get_local_telemetry()
    
    def __enter__(self):
        self.span_context = self.telemetry.start_span(self.span_name, self.attributes)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # Add error information to attributes
            self.attributes.update({
                'error': True,
                'error_type': exc_type.__name__ if exc_type else None,
                'error_message': str(exc_val) if exc_val else None
            })
        
        self.telemetry.end_span(self.span_context, self.attributes)
    
    def set_attribute(self, key: str, value: Any):
        """Set an attribute on the current span"""
        if self.span_context:
            self.span_context['attributes'][key] = value


# Convenience function for tracking events
def track_local_event(event_name: str, distinct_id: str, properties: Dict[str, Any] = None):
    """Convenience function to track events locally"""
    telemetry = get_local_telemetry()
    telemetry.track_event(event_name, distinct_id, properties) 