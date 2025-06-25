"""
Email Redirection Models - Privacy-First Email Storage
Stores all emails that would have been sent externally in local database for admin viewing.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from .base import BaseModel

User = get_user_model()


class RedirectedEmail(BaseModel):
    """
    Store emails that were intercepted and redirected to local storage
    instead of being sent to external email services
    """
    
    # Email metadata
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_email = models.EmailField(help_text="Intended recipient email address")
    from_email = models.EmailField(help_text="Sender email address")
    subject = models.CharField(max_length=500, help_text="Email subject line")
    
    # Email content
    html_content = models.TextField(help_text="HTML email content")
    text_content = models.TextField(blank=True, null=True, help_text="Plain text email content")
    
    # Email classification
    email_type = models.CharField(
        max_length=100,
        choices=[
            ('auth', 'Authentication'),
            ('notification', 'Notification'),
            ('invitation', 'Invitation'),
            ('system', 'System'),
            ('webhook', 'Webhook'),
            ('other', 'Other'),
        ],
        default='other',
        help_text="Type of email for categorization"
    )
    
    # Privacy tracking
    original_destination = models.CharField(
        max_length=255,
        help_text="Original external service that would have sent this email"
    )
    
    # Status tracking
    status = models.CharField(
        max_length=50,
        choices=[
            ('intercepted', 'Intercepted'),
            ('stored', 'Stored Locally'),
            ('viewed', 'Viewed in Admin'),
            ('exported', 'Exported'),
        ],
        default='intercepted'
    )
    
    # Associated user (if applicable)
    related_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User this email was intended for"
    )
    
    # Metadata
    headers = models.JSONField(
        default=dict,
        help_text="Email headers as JSON"
    )
    
    # Timing
    intended_send_time = models.DateTimeField(
        auto_now_add=True,
        help_text="When this email would have been sent"
    )
    
    # Security flags
    contains_sensitive_data = models.BooleanField(
        default=False,
        help_text="Whether this email contains sensitive information"
    )
    
    external_links_removed = models.BooleanField(
        default=False,
        help_text="Whether external links were sanitized"
    )
    
    class Meta:
        verbose_name = "Redirected Email"
        verbose_name_plural = "Redirected Emails"
        db_table = "redirected_emails"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["to_email"]),
            models.Index(fields=["email_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]
    
    def __str__(self):
        return f"Email to {self.to_email}: {self.subject[:50]}..."
    
    @property
    def is_recent(self):
        """Check if email was created in the last 24 hours"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at > timezone.now() - timedelta(days=1)
    
    def mark_as_viewed(self):
        """Mark email as viewed in admin dashboard"""
        if self.status == 'stored':
            self.status = 'viewed'
            self.save(update_fields=['status', 'updated_at'])


class EmailRedirectionStats(BaseModel):
    """
    Statistics about email redirections for dashboard display
    """
    
    date = models.DateField(unique=True, help_text="Date for these statistics")
    
    # Counts by type
    total_emails_intercepted = models.PositiveIntegerField(default=0)
    auth_emails = models.PositiveIntegerField(default=0)
    notification_emails = models.PositiveIntegerField(default=0)
    invitation_emails = models.PositiveIntegerField(default=0)
    system_emails = models.PositiveIntegerField(default=0)
    webhook_emails = models.PositiveIntegerField(default=0)
    other_emails = models.PositiveIntegerField(default=0)
    
    # External services that would have been used
    external_services_blocked = models.JSONField(
        default=dict,
        help_text="Count of emails by external service that was blocked"
    )
    
    # Privacy metrics
    sensitive_emails_secured = models.PositiveIntegerField(default=0)
    external_links_sanitized = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Email Redirection Statistics"
        verbose_name_plural = "Email Redirection Statistics"
        db_table = "email_redirection_stats"
        ordering = ["-date"]
    
    def __str__(self):
        return f"Email stats for {self.date}: {self.total_emails_intercepted} intercepted" 