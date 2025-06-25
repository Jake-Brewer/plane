# Python imports
import os
import atexit
import logging

# Local imports - redirect telemetry to local database
from plane.utils.local_telemetry import (
    init_local_telemetry,
    shutdown_local_telemetry,
    get_local_telemetry,
    LocalTelemetrySpan
)

logger = logging.getLogger(__name__)

# Global variable to track initialization
_TRACER_PROVIDER = None


def init_tracer():
    """
    Initialize local telemetry service instead of OpenTelemetry
    PRIVACY: This replaces external data exfiltration to telemetry.plane.so
    """
    global _TRACER_PROVIDER

    # If already initialized, return existing provider
    if _TRACER_PROVIDER is not None:
        return _TRACER_PROVIDER

    logger.info("PRIVACY: Initializing LOCAL telemetry (no external data sent)")
    
    # Initialize local telemetry service instead of OpenTelemetry
    _TRACER_PROVIDER = init_local_telemetry()

    # Register shutdown handler
    atexit.register(shutdown_tracer)

    logger.info("PRIVACY: Local telemetry initialized - data stays on your server")
    return _TRACER_PROVIDER


def shutdown_tracer():
    """Shutdown local telemetry service"""
    global _TRACER_PROVIDER

    if _TRACER_PROVIDER is not None:
        logger.info("PRIVACY: Shutting down local telemetry service")
        shutdown_local_telemetry()
        _TRACER_PROVIDER = None


def get_tracer(name: str = "plane-api"):
    """
    Get a tracer instance (compatibility function)
    Returns a wrapper that creates local telemetry spans
    """
    if _TRACER_PROVIDER is None:
        init_tracer()
    
    return LocalTelemetryTracer(name)


class LocalTelemetryTracer:
    """
    Tracer compatibility class that creates local telemetry spans
    Replaces OpenTelemetry tracer to prevent external data exfiltration
    """
    
    def __init__(self, name: str):
        self.name = name
        self.telemetry = get_local_telemetry()
    
    def start_span(self, span_name: str, attributes=None):
        """Start a local telemetry span"""
        return LocalTelemetrySpan(span_name, attributes or {})
    
    def start_as_current_span(self, span_name: str, attributes=None):
        """Start a span as current span (context manager)"""
        return LocalTelemetrySpan(span_name, attributes or {})


# Compatibility functions for existing code
def trace_instance_details(instance_data):
    """
    Trace instance details locally instead of sending to plane.so
    """
    try:
        with LocalTelemetrySpan("instance_details", instance_data) as span:
            span.set_attribute("traced_locally", True)
            span.set_attribute("privacy_mode", "local_only")
            logger.info("PRIVACY: Instance telemetry stored locally")
    except Exception as e:
        logger.error(f"LOCAL_TELEMETRY: Failed to trace instance details: {e}")


def trace_workspace_details(workspace_data):
    """
    Trace workspace details locally instead of sending to plane.so
    """
    try:
        with LocalTelemetrySpan("workspace_details", workspace_data) as span:
            span.set_attribute("traced_locally", True)
            span.set_attribute("privacy_mode", "local_only")
            logger.info("PRIVACY: Workspace telemetry stored locally")
    except Exception as e:
        logger.error(f"LOCAL_TELEMETRY: Failed to trace workspace details: {e}")


# Environment variable override for external telemetry
def is_external_telemetry_disabled():
    """
    Check if external telemetry is disabled
    Returns True to indicate we're using local telemetry only
    """
    return True  # Always return True - we never send external telemetry


def get_telemetry_endpoint():
    """
    Return the telemetry endpoint (local database)
    """
    return "local://database"  # Indicate local storage


# Backwards compatibility
def get_otel_endpoint():
    """Backwards compatibility - returns local endpoint"""
    return "local://database"


# Initialize on import if environment variable is set
if os.environ.get("PLANE_TELEMETRY_ENABLED", "true").lower() == "true":
    logger.info("PRIVACY: Plane telemetry enabled - using LOCAL storage only")
    init_tracer()
else:
    logger.info("PRIVACY: Plane telemetry disabled via environment variable")
