# Django imports
from django.db import models
from django.contrib.postgres.fields import JSONField

# Module imports
from plane.db.models import BaseModel


class LocalTelemetryData(BaseModel):
    """Store OpenTelemetry data locally instead of sending to telemetry.plane.so"""
    
    # Instance identification
    instance_id = models.CharField(max_length=255, db_index=True)
    instance_name = models.CharField(max_length=255, null=True, blank=True)
    
    # Telemetry metadata
    span_name = models.CharField(max_length=255)  # e.g., "instance_details", "workspace_details"
    trace_id = models.CharField(max_length=255, null=True, blank=True)
    span_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Telemetry attributes (stored as JSON)
    attributes = JSONField(default=dict)
    
    # Timing information
    start_time = models.DateTimeField(auto_now_add=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    
    # Instance metadata
    current_version = models.CharField(max_length=100, null=True, blank=True)
    latest_version = models.CharField(max_length=100, null=True, blank=True)
    edition = models.CharField(max_length=50, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    
    # Usage statistics
    user_count = models.IntegerField(default=0)
    workspace_count = models.IntegerField(default=0)
    project_count = models.IntegerField(default=0)
    issue_count = models.IntegerField(default=0)
    module_count = models.IntegerField(default=0)
    cycle_count = models.IntegerField(default=0)
    page_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Local Telemetry Data"
        verbose_name_plural = "Local Telemetry Data"
        db_table = "local_telemetry_data"
        indexes = [
            models.Index(fields=['instance_id', 'created_at']),
            models.Index(fields=['span_name', 'created_at']),
        ]

    def __str__(self):
        return f"{self.instance_name} - {self.span_name} ({self.created_at})"


class LocalWorkspaceTelemetry(BaseModel):
    """Store workspace-specific telemetry data locally"""
    
    # Related to main telemetry record
    telemetry_data = models.ForeignKey(
        LocalTelemetryData, 
        on_delete=models.CASCADE, 
        related_name='workspace_data'
    )
    
    # Workspace identification
    workspace_id = models.UUIDField(db_index=True)
    workspace_slug = models.CharField(max_length=255)
    
    # Workspace usage statistics
    project_count = models.IntegerField(default=0)
    issue_count = models.IntegerField(default=0)
    module_count = models.IntegerField(default=0)
    cycle_count = models.IntegerField(default=0)
    cycle_issue_count = models.IntegerField(default=0)
    module_issue_count = models.IntegerField(default=0)
    page_count = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Local Workspace Telemetry"
        verbose_name_plural = "Local Workspace Telemetry"
        db_table = "local_workspace_telemetry"
        indexes = [
            models.Index(fields=['workspace_id', 'created_at']),
        ]

    def __str__(self):
        return f"Workspace {self.workspace_slug} - {self.created_at}"


class LocalAnalyticsEvent(BaseModel):
    """Store PostHog-style analytics events locally"""
    
    # Event identification
    event_name = models.CharField(max_length=255, db_index=True)
    distinct_id = models.CharField(max_length=255, db_index=True)  # User/session ID
    
    # Event properties (JSON field for flexibility)
    properties = JSONField(default=dict)
    
    # User/session context
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    workspace_id = models.UUIDField(null=True, blank=True, db_index=True)
    project_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Request context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    
    # Geographic data (if available)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = "Local Analytics Event"
        verbose_name_plural = "Local Analytics Events"
        db_table = "local_analytics_events"
        indexes = [
            models.Index(fields=['event_name', 'created_at']),
            models.Index(fields=['distinct_id', 'created_at']),
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['workspace_id', 'created_at']),
        ]

    def __str__(self):
        return f"{self.event_name} - {self.distinct_id} ({self.created_at})"


class LocalFrontendMetrics(BaseModel):
    """Store frontend performance metrics locally (for our MCP analytics)"""
    
    # Page/route information
    route = models.CharField(max_length=500, db_index=True)
    url = models.URLField()
    
    # Performance metrics
    load_time_ms = models.IntegerField()  # Total page load time
    dom_content_loaded_ms = models.IntegerField(null=True, blank=True)
    first_paint_ms = models.IntegerField(null=True, blank=True)
    first_contentful_paint_ms = models.IntegerField(null=True, blank=True)
    time_to_interactive_ms = models.IntegerField(null=True, blank=True)
    
    # Core Web Vitals
    largest_contentful_paint_ms = models.IntegerField(null=True, blank=True)
    cumulative_layout_shift = models.FloatField(null=True, blank=True)
    first_input_delay_ms = models.IntegerField(null=True, blank=True)
    
    # Error tracking
    chunk_errors = JSONField(default=list)  # List of ChunkLoadErrors
    javascript_errors = JSONField(default=list)  # List of JS errors
    
    # User context
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    workspace_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Browser/device context
    user_agent = models.TextField(null=True, blank=True)
    viewport_width = models.IntegerField(null=True, blank=True)
    viewport_height = models.IntegerField(null=True, blank=True)
    connection_type = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name = "Local Frontend Metrics"
        verbose_name_plural = "Local Frontend Metrics"
        db_table = "local_frontend_metrics"
        indexes = [
            models.Index(fields=['route', 'created_at']),
            models.Index(fields=['load_time_ms', 'created_at']),
            models.Index(fields=['user_id', 'created_at']),
        ]

    def __str__(self):
        return f"{self.route} - {self.load_time_ms}ms ({self.created_at})"


class LocalSystemHealth(BaseModel):
    """Store system health and monitoring data locally"""
    
    # System identification
    component = models.CharField(max_length=100, db_index=True)  # e.g., "web", "api", "worker"
    instance_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Health metrics
    status = models.CharField(max_length=20, choices=[
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ], default='healthy')
    
    # Performance metrics
    cpu_usage_percent = models.FloatField(null=True, blank=True)
    memory_usage_percent = models.FloatField(null=True, blank=True)
    disk_usage_percent = models.FloatField(null=True, blank=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    # Database metrics
    db_connections_active = models.IntegerField(null=True, blank=True)
    db_query_time_avg_ms = models.FloatField(null=True, blank=True)
    
    # Additional metrics (JSON for flexibility)
    metrics = JSONField(default=dict)
    
    # Error information
    error_message = models.TextField(null=True, blank=True)
    error_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Local System Health"
        verbose_name_plural = "Local System Health"
        db_table = "local_system_health"
        indexes = [
            models.Index(fields=['component', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"{self.component} - {self.status} ({self.created_at})" 