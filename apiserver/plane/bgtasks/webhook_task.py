import hashlib
import hmac
import json
import logging
import uuid
from datetime import datetime
from urllib.parse import urlparse

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# LOCAL ANALYTICS: Webhook security enhancement
# ORIGINAL PURPOSE: Send project data to external webhook URLs for integrations
# ORIGINAL RISK: Could send ALL project data to any external service
# REPLACEMENT: Localhost-only webhook system with comprehensive logging
# VALUE PRESERVED: Webhook functionality for local integrations and development
# DATA PRIVACY: All webhook data logged locally, external URLs blocked
# ADMIN VISIBILITY: All webhook attempts visible in admin dashboard with original destinations

from plane.app.serializers import (
    CycleSerializer,
    IssueCommentSerializer,
    IssueSerializer,
    ModuleSerializer,
    ProjectSerializer,
)
from plane.db.models import (
    Cycle,
    Issue,
    IssueComment,
    Module,
    Project,
    User,
    Webhook,
    WebhookLog,
)
from plane.utils.exception_logger import log_exception
from plane.utils.integrations import get_email_configuration


# Local webhook security validator
class LocalWebhookValidator:
    """
    Security validator to ensure webhooks only point to localhost
    and log all attempts for admin visibility
    """
    
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '::1'  # IPv6 localhost
    ]
    
    @classmethod
    def validate_webhook_url(cls, url: str) -> tuple[bool, str, str]:
        """
        Validate webhook URL to ensure it only points to localhost
        
        Returns:
            (is_valid, safe_url, original_url)
        """
        original_url = url
        
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            # Check if hostname is in allowed hosts
            if hostname and hostname.lower() in cls.ALLOWED_HOSTS:
                return True, url, original_url
            
            # Block external URLs and redirect to local webhook receiver
            safe_url = "http://localhost:8000/api/webhooks/local-receiver/"
            
            # Log the blocked attempt
            cls.log_blocked_webhook(original_url, safe_url)
            
            return False, safe_url, original_url
            
        except Exception as e:
            # Invalid URL, redirect to local receiver
            safe_url = "http://localhost:8000/api/webhooks/local-receiver/"
            cls.log_blocked_webhook(original_url, safe_url, str(e))
            return False, safe_url, original_url
    
    @classmethod
    def log_blocked_webhook(cls, original_url: str, safe_url: str, error: str = None):
        """Log blocked webhook attempts for admin visibility"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'original_url': original_url,
            'redirected_to': safe_url,
            'reason': 'External URL blocked for data privacy',
            'error': error,
            'security_policy': 'localhost-only'
        }
        
        # Log to console for immediate visibility
        print(f"[WEBHOOK SECURITY] Blocked external webhook: {original_url} -> {safe_url}")
        
        # Store in local analytics for admin dashboard
        try:
            import os
            import json
            log_dir = os.path.join(settings.BASE_DIR, 'logs', 'local-analytics')
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, 'blocked-webhooks.json')
            existing_logs = []
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            
            existing_logs.append(log_entry)
            
            # Keep only last 1000 entries
            if len(existing_logs) > 1000:
                existing_logs = existing_logs[-1000:]
            
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
                
        except Exception as e:
            print(f"[WEBHOOK SECURITY] Failed to log blocked webhook: {e}")


def get_model_data(event, event_id, many=False):
    model_data = None
    if event == "issue":
        if many:
            model_data = Issue.objects.filter(pk__in=event_id).values(
                "id",
                "name",
                "state_id",
                "sort_order",
                "completed_at",
                "estimate_point",
                "priority",
                "start_date",
                "target_date",
                "sequence_id",
                "project_id",
            )
        else:
            model_data = IssueSerializer(Issue.objects.get(pk=event_id)).data
    if event == "cycle":
        model_data = CycleSerializer(Cycle.objects.get(pk=event_id)).data
    if event == "module":
        model_data = ModuleSerializer(Module.objects.get(pk=event_id)).data
    if event == "project":
        model_data = ProjectSerializer(Project.objects.get(pk=event_id)).data
    if event == "issue_comment":
        model_data = IssueCommentSerializer(IssueComment.objects.get(pk=event_id)).data

    return model_data


@shared_task(
    bind=True,
    autoretry_for=(requests.RequestException,),
    retry_backoff=600,
    max_retries=5,
    retry_jitter=True,
)
def webhook_task(self, webhook, slug, event, event_data, action, current_site):
    try:
        webhook = Webhook.objects.get(id=webhook, workspace__slug=slug)

        # SECURITY: Validate webhook URL to ensure localhost-only
        is_valid, safe_url, original_url = LocalWebhookValidator.validate_webhook_url(webhook.url)
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Plane-Local-Webhook",
            "X-Plane-Delivery": str(uuid.uuid4()),
            "X-Plane-Event": event,
            "X-Plane-Original-URL": original_url,  # Track original destination
            "X-Plane-Security-Policy": "localhost-only",
        }

        # Add security warning header if URL was blocked
        if not is_valid:
            headers["X-Plane-Security-Warning"] = f"External URL blocked: {original_url}"

        # Your secret key
        event_data = (
            json.loads(json.dumps(event_data, cls=DjangoJSONEncoder))
            if event_data is not None
            else None
        )

        action = {
            "POST": "create",
            "PATCH": "update",
            "PUT": "update",
            "DELETE": "delete",
        }.get(action, action)

        payload = {
            "event": event,
            "action": action,
            "webhook_id": str(webhook.id),
            "workspace_id": str(webhook.workspace_id),
            "data": event_data,
            "security_info": {
                "original_url": original_url,
                "is_external_blocked": not is_valid,
                "policy": "localhost-only",
                "timestamp": datetime.now().isoformat()
            }
        }

        # Use HMAC for generating signature
        if webhook.secret_key:
            hmac_signature = hmac.new(
                webhook.secret_key.encode("utf-8"),
                json.dumps(payload).encode("utf-8"),
                hashlib.sha256,
            )
            signature = hmac_signature.hexdigest()
            headers["X-Plane-Signature"] = signature

        # Send the webhook event to safe URL only
        response = requests.post(safe_url, headers=headers, json=payload, timeout=30)

        # Log the webhook request with security info
        WebhookLog.objects.create(
            workspace_id=str(webhook.workspace_id),
            webhook_id=str(webhook.id),
            event_type=str(event),
            request_method=str(action),
            request_headers=str(headers),
            request_body=str(payload),
            response_status=str(response.status_code),
            response_headers=str(response.headers),
            response_body=str(response.text),
            retry_count=str(self.request.retries),
        )

        # Log security event for admin visibility
        if not is_valid:
            print(f"[WEBHOOK SECURITY] Redirected external webhook {original_url} to {safe_url}")

    except Webhook.DoesNotExist:
        return
    except requests.RequestException as e:
        # Log the failed webhook request
        WebhookLog.objects.create(
            workspace_id=str(webhook.workspace_id),
            webhook_id=str(webhook.id),
            event_type=str(event),
            request_method=str(action),
            request_headers=str(headers),
            request_body=str(payload),
            response_status=500,
            response_headers="",
            response_body=str(e),
            retry_count=str(self.request.retries),
        )
        # Retry logic
        if self.request.retries >= self.max_retries:
            Webhook.objects.filter(pk=webhook.id).update(is_active=False)
            if webhook:
                # send email for the deactivation of the webhook
                send_webhook_deactivation_email(
                    webhook_id=webhook.id,
                    receiver_id=webhook.created_by_id,
                    reason=str(e),
                    current_site=current_site,
                )
            return
        raise requests.RequestException()

    except Exception as e:
        if settings.DEBUG:
            print(e)
        log_exception(e)
        return


@shared_task
def send_webhook_deactivation_email(webhook_id, receiver_id, current_site, reason):
    # Get email configurations
    (
        EMAIL_HOST,
        EMAIL_HOST_USER,
        EMAIL_HOST_PASSWORD,
        EMAIL_PORT,
        EMAIL_USE_TLS,
        EMAIL_USE_SSL,
        EMAIL_FROM,
    ) = get_email_configuration()

    receiver = User.objects.get(pk=receiver_id)
    webhook = Webhook.objects.get(pk=webhook_id)
    subject = "Webhook Deactivated"
    
    # Enhanced message with security info
    message = f"Webhook {webhook.url} has been deactivated due to failed requests. Note: External webhooks are blocked for data privacy - only localhost URLs are allowed."

    # Send the mail
    context = {
        "email": receiver.email,
        "message": message,
        "webhook_url": f"{current_site}/{str(webhook.workspace.slug)}/settings/webhooks/{str(webhook.id)}",
        "security_policy": "Webhooks are restricted to localhost for data privacy protection"
    }
    html_content = render_to_string(
        "emails/notifications/webhook-deactivate.html", context
    )
    text_content = strip_tags(html_content)

    try:
        connection = get_connection(
            host=EMAIL_HOST,
            port=int(EMAIL_PORT),
            username=EMAIL_HOST_USER,
            password=EMAIL_HOST_PASSWORD,
            use_tls=EMAIL_USE_TLS == "1",
            use_ssl=EMAIL_USE_SSL == "1",
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=EMAIL_FROM,
            to=[receiver.email],
            connection=connection,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logging.getLogger("plane").info("Email sent successfully.")
        return
    except Exception as e:
        log_exception(e)
        return


@shared_task(
    bind=True,
    autoretry_for=(requests.RequestException,),
    retry_backoff=600,
    max_retries=5,
    retry_jitter=True,
)
def webhook_send_task(
    self, webhook, slug, event, event_data, action, current_site, activity
):
    try:
        webhook = Webhook.objects.get(id=webhook, workspace__slug=slug)

        # SECURITY: Validate webhook URL to ensure localhost-only
        is_valid, safe_url, original_url = LocalWebhookValidator.validate_webhook_url(webhook.url)

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Plane-Local-Webhook",
            "X-Plane-Delivery": str(uuid.uuid4()),
            "X-Plane-Event": event,
            "X-Plane-Original-URL": original_url,  # Track original destination
            "X-Plane-Security-Policy": "localhost-only",
        }

        # Add security warning header if URL was blocked
        if not is_valid:
            headers["X-Plane-Security-Warning"] = f"External URL blocked: {original_url}"

        # # Your secret key
        event_data = (
            json.loads(json.dumps(event_data, cls=DjangoJSONEncoder))
            if event_data is not None
            else None
        )

        activity = (
            json.loads(json.dumps(activity, cls=DjangoJSONEncoder))
            if activity is not None
            else None
        )

        action = {
            "POST": "create",
            "PATCH": "update",
            "PUT": "update",
            "DELETE": "delete",
        }.get(action, action)

        payload = {
            "event": event,
            "action": action,
            "webhook_id": str(webhook.id),
            "workspace_id": str(webhook.workspace_id),
            "data": event_data,
            "activity": activity,
            "security_info": {
                "original_url": original_url,
                "is_external_blocked": not is_valid,
                "policy": "localhost-only",
                "timestamp": datetime.now().isoformat()
            }
        }

        # Use HMAC for generating signature
        if webhook.secret_key:
            hmac_signature = hmac.new(
                webhook.secret_key.encode("utf-8"),
                json.dumps(payload).encode("utf-8"),
                hashlib.sha256,
            )
            signature = hmac_signature.hexdigest()
            headers["X-Plane-Signature"] = signature

        # Send the webhook event to safe URL only
        response = requests.post(safe_url, headers=headers, json=payload, timeout=30)

        # Log the webhook request with security info
        WebhookLog.objects.create(
            workspace_id=str(webhook.workspace_id),
            webhook_id=str(webhook.id),
            event_type=str(event),
            request_method=str(action),
            request_headers=str(headers),
            request_body=str(payload),
            response_status=str(response.status_code),
            response_headers=str(response.headers),
            response_body=str(response.text),
            retry_count=str(self.request.retries),
        )

        # Log security event for admin visibility
        if not is_valid:
            print(f"[WEBHOOK SECURITY] Redirected external webhook {original_url} to {safe_url}")

    except requests.RequestException as e:
        # Log the failed webhook request
        WebhookLog.objects.create(
            workspace_id=str(webhook.workspace_id),
            webhook_id=str(webhook.id),
            event_type=str(event),
            request_method=str(action),
            request_headers=str(headers),
            request_body=str(payload),
            response_status=500,
            response_headers="",
            response_body=str(e),
            retry_count=str(self.request.retries),
        )
        # Retry logic
        if self.request.retries >= self.max_retries:
            Webhook.objects.filter(pk=webhook.id).update(is_active=False)
            if webhook:
                # send email for the deactivation of the webhook
                send_webhook_deactivation_email(
                    webhook_id=webhook.id,
                    receiver_id=webhook.created_by_id,
                    reason=str(e),
                    current_site=current_site,
                )
            return
        raise requests.RequestException()

    except Exception as e:
        if settings.DEBUG:
            print(e)
        log_exception(e)
        return


@shared_task
def webhook_activity(
    event,
    verb,
    field,
    old_value,
    new_value,
    actor_id,
    slug,
    current_site,
    event_id,
    old_identifier,
    new_identifier,
):
    try:
        webhooks = Webhook.objects.filter(workspace__slug=slug, is_active=True)

        if event == "project":
            webhooks = webhooks.filter(project=True)

        if event == "issue":
            webhooks = webhooks.filter(issue=True)

        if event == "module" or event == "module_issue":
            webhooks = webhooks.filter(module=True)

        if event == "cycle" or event == "cycle_issue":
            webhooks = webhooks.filter(cycle=True)

        if event == "issue_comment":
            webhooks = webhooks.filter(issue_comment=True)

        for webhook in webhooks:
            webhook_send_task.delay(
                webhook=webhook.id,
                slug=slug,
                event=event,
                event_data=get_model_data(event=event, event_id=event_id),
                action=verb,
                current_site=current_site,
                activity={
                    "field": field,
                    "new_value": new_value,
                    "old_value": old_value,
                    "actor": get_model_data(event="user", event_id=actor_id),
                    "old_identifier": old_identifier,
                    "new_identifier": new_identifier,
                },
            )
        return
    except Exception as e:
        # Return if a does not exist error occurs
        if isinstance(e, ObjectDoesNotExist):
            return
        if settings.DEBUG:
            print(e)
        log_exception(e)
        return


@shared_task
def model_activity(
    model_name, model_id, requested_data, current_instance, actor_id, slug, origin=None
):
    """Function takes in two json and computes differences between keys of both the json"""
    if current_instance is None:
        webhook_activity.delay(
            event=model_name,
            verb="created",
            field=None,
            old_value=None,
            new_value=None,
            actor_id=actor_id,
            slug=slug,
            current_site=origin,
            event_id=model_id,
            old_identifier=None,
            new_identifier=None,
        )
        return

    # Load the current instance
    current_instance = (
        json.loads(current_instance) if current_instance is not None else None
    )

    # Loop through all keys in requested data and check the current value and requested value
    for key in requested_data:
        # Check if key is present in current instance or not
        if key in current_instance:
            current_value = current_instance.get(key, None)
            requested_value = requested_data.get(key, None)
            if current_value != requested_value:
                webhook_activity.delay(
                    event=model_name,
                    verb="updated",
                    field=key,
                    old_value=current_value,
                    new_value=requested_value,
                    actor_id=actor_id,
                    slug=slug,
                    current_site=origin,
                    event_id=model_id,
                    old_identifier=None,
                    new_identifier=None,
                )

    return
