import os
import logging
import uuid

# third party imports
from celery import shared_task
from posthog import Posthog

# module imports
from plane.license.utils.instance_value import get_configuration_value
from plane.utils.exception_logger import log_exception
from plane.utils.local_telemetry import track_local_event

# Django imports
from django.conf import settings

logger = logging.getLogger(__name__)


def posthogConfiguration():
    """
    PRIVACY: This function now returns None to disable external PostHog
    All analytics are stored locally in the database instead
    """
    logger.info("PRIVACY: PostHog external analytics disabled - using local storage")
    return None, None  # Always return None to prevent external data sending


@shared_task
def auth_events(user, email, user_agent, ip, event_name, medium, first_time):
    try:
        POSTHOG_API_KEY, POSTHOG_HOST = posthogConfiguration()

        if POSTHOG_API_KEY and POSTHOG_HOST:
            posthog = Posthog(POSTHOG_API_KEY, host=POSTHOG_HOST)
            posthog.capture(
                email,
                event=event_name,
                properties={
                    "event_id": uuid.uuid4().hex,
                    "user": {"email": email, "id": str(user)},
                    "device_ctx": {"ip": ip, "user_agent": user_agent},
                    "medium": medium,
                    "first_time": first_time,
                },
            )
    except Exception as e:
        log_exception(e)
        return


@shared_task
def workspace_invite_event(user, email, slug, current_site):
    """
    Track workspace invite event locally instead of sending to PostHog
    """
    try:
        # Prepare event data for local storage
        event_properties = {
            'user_id': str(user.id) if user else None,
            'email': email,
            'workspace_slug': slug,
            'domain': current_site,
            'event_type': 'workspace_invite',
            'ip_address': None,  # Could be extracted from request
        }
        
        # Track event locally
        track_local_event(
            event_name="workspace_invite",
            distinct_id=email,
            properties=event_properties
        )
        
        logger.info(f"PRIVACY: Workspace invite event stored locally for {email}")
        
    except Exception as e:
        logger.error(f"LOCAL_ANALYTICS: Failed to track workspace invite: {e}")


def user_signin_event(user, email, current_site):
    """
    Track user signin event locally instead of sending to PostHog
    """
    try:
        # Prepare event data for local storage
        event_properties = {
            'user_id': str(user.id) if user else None,
            'email': email,
            'domain': current_site,
            'event_type': 'user_signin',
            'user_name': getattr(user, 'display_name', '') if user else '',
        }
        
        # Track event locally
        track_local_event(
            event_name="user_signin",
            distinct_id=str(user.id) if user else email,
            properties=event_properties
        )
        
        logger.info(f"PRIVACY: User signin event stored locally for {email}")
        
    except Exception as e:
        logger.error(f"LOCAL_ANALYTICS: Failed to track user signin: {e}")


def track_custom_event(event_name, user_id, properties=None):
    """
    Track custom event locally instead of sending to PostHog
    """
    try:
        # Prepare event data for local storage
        event_properties = properties or {}
        event_properties.update({
            'user_id': str(user_id) if user_id else None,
            'event_type': 'custom',
            'tracked_locally': True,
        })
        
        # Track event locally
        track_local_event(
            event_name=event_name,
            distinct_id=str(user_id) if user_id else 'anonymous',
            properties=event_properties
        )
        
        logger.info(f"PRIVACY: Custom event '{event_name}' stored locally")
        
    except Exception as e:
        logger.error(f"LOCAL_ANALYTICS: Failed to track custom event: {e}")


def track_workspace_activity(workspace_id, activity_type, user_id=None, properties=None):
    """
    Track workspace activity locally
    """
    try:
        # Prepare event data for local storage
        event_properties = properties or {}
        event_properties.update({
            'workspace_id': str(workspace_id),
            'activity_type': activity_type,
            'user_id': str(user_id) if user_id else None,
            'event_type': 'workspace_activity',
        })
        
        # Track event locally
        track_local_event(
            event_name=f"workspace_{activity_type}",
            distinct_id=str(user_id) if user_id else str(workspace_id),
            properties=event_properties
        )
        
        logger.debug(f"PRIVACY: Workspace activity '{activity_type}' stored locally")
        
    except Exception as e:
        logger.error(f"LOCAL_ANALYTICS: Failed to track workspace activity: {e}")


# Backwards compatibility - these functions now store data locally
def posthog_capture(event_name, distinct_id, properties=None):
    """
    Backwards compatibility function - captures events locally
    """
    track_local_event(event_name, distinct_id, properties)


def is_posthog_enabled():
    """
    Returns False to indicate PostHog external tracking is disabled
    """
    return False  # Always False - we use local analytics only


def get_posthog_settings():
    """
    Returns empty settings since PostHog is disabled
    """
    return {
        'enabled': False,
        'api_key': None,
        'host': None,
        'privacy_mode': 'local_only',
        'message': 'Analytics stored locally in database'
    }
