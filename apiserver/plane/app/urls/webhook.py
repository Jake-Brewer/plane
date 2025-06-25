from django.urls import path

from plane.app.views import (
    WebhookEndpoint,
    WebhookLogsEndpoint,
    WebhookSecretRegenerateEndpoint,
)
# LOCAL ANALYTICS: Import local webhook receiver
from plane.api.views.webhook import local_webhook_receiver


urlpatterns = [
    path("workspaces/<str:slug>/webhooks/", WebhookEndpoint.as_view(), name="webhooks"),
    path(
        "workspaces/<str:slug>/webhooks/<uuid:pk>/",
        WebhookEndpoint.as_view(),
        name="webhooks",
    ),
    path(
        "workspaces/<str:slug>/webhooks/<uuid:pk>/regenerate/",
        WebhookSecretRegenerateEndpoint.as_view(),
        name="webhooks",
    ),
    path(
        "workspaces/<str:slug>/webhook-logs/<uuid:webhook_id>/",
        WebhookLogsEndpoint.as_view(),
        name="webhooks",
    ),
    # LOCAL ANALYTICS: Local webhook receiver for security
    path(
        "webhooks/local-receiver/",
        local_webhook_receiver,
        name="local_webhook_receiver",
    ),
]
