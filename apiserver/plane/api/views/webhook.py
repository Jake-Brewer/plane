# LOCAL ANALYTICS: Local webhook receiver for security
# ORIGINAL PURPOSE: N/A - New security feature
# REPLACEMENT: Localhost webhook receiver that logs all webhook data
# VALUE PRESERVED: Webhook functionality without external data transmission
# DATA PRIVACY: All webhook data stored locally for admin visibility
# ADMIN VISIBILITY: All webhook payloads accessible through admin dashboard

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json
import os
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])
def local_webhook_receiver(request):
    """
    Local webhook receiver that logs all webhook data for admin visibility
    This endpoint receives all webhooks that would have been sent externally
    """
    try:
        # Parse webhook data
        webhook_data = {
            'timestamp': datetime.now().isoformat(),
            'headers': dict(request.headers),
            'body': json.loads(request.body) if request.body else {},
            'method': request.method,
            'path': request.path,
            'remote_addr': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
        }
        
        # Log to local analytics for admin dashboard
        log_dir = os.path.join(settings.BASE_DIR, 'logs', 'local-analytics')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'received-webhooks.json')
        existing_logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                existing_logs = json.load(f)
        
        existing_logs.append(webhook_data)
        
        # Keep only last 1000 entries
        if len(existing_logs) > 1000:
            existing_logs = existing_logs[-1000:]
        
        with open(log_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)
        
        # Log to console for immediate visibility
        original_url = request.headers.get('X-Plane-Original-URL', 'unknown')
        security_warning = request.headers.get('X-Plane-Security-Warning')
        
        print(f"[LOCAL WEBHOOK] Received webhook from original URL: {original_url}")
        if security_warning:
            print(f"[WEBHOOK SECURITY] {security_warning}")
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'message': 'Webhook received and logged locally',
            'timestamp': webhook_data['timestamp'],
            'security_policy': 'localhost-only',
            'admin_access': 'View webhook data in admin dashboard'
        })
        
    except Exception as e:
        print(f"[LOCAL WEBHOOK] Error processing webhook: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'security_policy': 'localhost-only'
        }, status=500) 