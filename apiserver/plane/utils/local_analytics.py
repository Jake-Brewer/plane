#!/usr/bin/env python3
\"\"\"
Local Analytics Service - Privacy-First Data Storage
Replaces external analytics services (PostHog, Sentry, Clarity, etc.) with local storage.
All data that would have been sent to external services is stored locally in SQLite.
\"\"\"

import json
import sqlite3
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import uuid
import os
from datetime import timedelta

# Configuration
LOCAL_ANALYTICS_DB = Path(\"/var/lib/plane/analytics/analytics.db\")
LOCAL_ANALYTICS_DIR = Path(\"/var/lib/plane/analytics\")

class LocalAnalyticsService:
    \"\"\"
    Local analytics service that stores all data locally instead of sending to external services.
    
    Replaces:
    - PostHog (user behavior tracking) → local user_events table
    - Sentry (error monitoring) → local error_logs table  
    - Microsoft Clarity (session recording) → local session_recordings table
    - Plausible (web analytics) → local page_analytics table
    - OpenTelemetry (performance metrics) → local performance_metrics table
    - Plane.so telemetry → local plane_telemetry table
    \"\"\"
    
    def __init__(self, db_path: str = "/var/lib/plane/analytics/analytics.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        \"\"\"Ensure the database directory exists\"\"\"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self):
        \"\"\"Initialize the local analytics database with all required tables\"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(\"\"\"
                    -- User Events (replaces PostHog)
                    CREATE TABLE IF NOT EXISTS user_events (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        event_name TEXT NOT NULL,
                        properties TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        session_id TEXT,
                        original_destination TEXT DEFAULT 'app.posthog.com'
                    );
                    
                    -- Error Logs (replaces Sentry)  
                    CREATE TABLE IF NOT EXISTS error_logs (
                        id TEXT PRIMARY KEY,
                        error_type TEXT NOT NULL,
                        error_message TEXT NOT NULL,
                        stack_trace TEXT,
                        user_context TEXT,
                        request_context TEXT,
                        severity TEXT DEFAULT 'error',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        original_destination TEXT DEFAULT 'sentry.io'
                    );
                    
                    -- Session Recordings (replaces Microsoft Clarity)
                    CREATE TABLE IF NOT EXISTS session_recordings (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        session_data TEXT,
                        page_url TEXT,
                        duration_seconds INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        original_destination TEXT DEFAULT 'clarity.microsoft.com'
                    );
                    
                    -- Page Analytics (replaces Plausible)
                    CREATE TABLE IF NOT EXISTS page_analytics (
                        id TEXT PRIMARY KEY,
                        page_url TEXT NOT NULL,
                        referrer TEXT,
                        user_agent TEXT,
                        session_id TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        original_destination TEXT DEFAULT 'plausible.io'
                    );
                    
                    -- Performance Metrics (replaces OpenTelemetry)
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id TEXT PRIMARY KEY,
                        metric_name TEXT NOT NULL,
                        metric_value REAL NOT NULL,
                        tags TEXT,
                        service_name TEXT DEFAULT 'plane',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        original_destination TEXT DEFAULT 'opentelemetry-collector'
                    );
                    
                    -- Plane Telemetry (replaces Plane.so telemetry)
                    CREATE TABLE IF NOT EXISTS plane_telemetry (
                        id TEXT PRIMARY KEY,
                        telemetry_type TEXT NOT NULL,
                        data TEXT,
                        instance_id TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        original_destination TEXT DEFAULT 'telemetry.plane.so'
                    );
                    
                    -- Create indexes for performance
                    CREATE INDEX IF NOT EXISTS idx_user_events_timestamp ON user_events(timestamp);
                    CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON error_logs(timestamp);
                    CREATE INDEX IF NOT EXISTS idx_session_recordings_timestamp ON session_recordings(timestamp);
                    CREATE INDEX IF NOT EXISTS idx_page_analytics_timestamp ON page_analytics(timestamp);
                    CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp);
                    CREATE INDEX IF NOT EXISTS idx_plane_telemetry_timestamp ON plane_telemetry(timestamp);
                \"\"\")
                logger.info(\"Local analytics database initialized successfully\")
        except Exception as e:
            logger.error(f\"Failed to initialize local analytics database: {e}\")
    
    def track_user_event(self, user_id: str, event_name: str, properties: Dict[str, Any] = None, session_id: str = None):
        \"\"\"
        Track user event locally (replaces PostHog)
        
        PRIVACY NOTE: Originally would be sent to app.posthog.com
        Now stored locally in user_events table
        \"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(\"\"\"
                    INSERT INTO user_events (id, user_id, event_name, properties, session_id)
                    VALUES (?, ?, ?, ?, ?)
                \"\"\", (
                    str(uuid.uuid4()),
                    user_id,
                    event_name,
                    json.dumps(properties or {}),
                    session_id
                ))
                logger.info(f\"User event tracked locally (was destined for PostHog): {event_name}\")
        except Exception as e:
            logger.error(f\"Failed to track user event locally: {e}\")
    
    def log_error(self, error_type: str, error_message: str, stack_trace: str = None, 
                  user_context: Dict[str, Any] = None, request_context: Dict[str, Any] = None, 
                  severity: str = 'error'):
        \"\"\"
        Log error locally (replaces Sentry)
        
        PRIVACY NOTE: Originally would be sent to sentry.io
        Now stored locally in error_logs table
        \"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(\"\"\"
                    INSERT INTO error_logs (id, error_type, error_message, stack_trace, user_context, request_context, severity)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                \"\"\", (
                    str(uuid.uuid4()),
                    error_type,
                    error_message,
                    stack_trace,
                    json.dumps(user_context or {}),
                    json.dumps(request_context or {}),
                    severity
                ))
                logger.info(f\"Error logged locally (was destined for Sentry): {error_type}\")
        except Exception as e:
            logger.error(f\"Failed to log error locally: {e}\")
    
    def record_session_data(self, user_id: str, session_data: Dict[str, Any], page_url: str, duration_seconds: int = 0):
        \"\"\"
        Record session data locally (replaces Microsoft Clarity)
        
        PRIVACY NOTE: Originally would be sent to clarity.microsoft.com
        Now stored locally in session_recordings table (metadata only, no screen recording)
        \"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(\"\"\"
                    INSERT INTO session_recordings (id, user_id, session_data, page_url, duration_seconds)
                    VALUES (?, ?, ?, ?, ?)
                \"\"\", (
                    str(uuid.uuid4()),
                    user_id,
                    json.dumps(session_data),
                    page_url,
                    duration_seconds
                ))
                logger.info(f\"Session data recorded locally (was destined for Clarity): {user_id}\")
        except Exception as e:
            logger.error(f\"Failed to record session data locally: {e}\")
    
    def track_page_view(self, page_url: str, referrer: str = None, user_agent: str = None, session_id: str = None):
        \"\"\"
        Track page view locally (replaces Plausible)
        
        PRIVACY NOTE: Originally would be sent to plausible.io
        Now stored locally in page_analytics table
        \"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(\"\"\"
                    INSERT INTO page_analytics (id, page_url, referrer, user_agent, session_id)
                    VALUES (?, ?, ?, ?, ?)
                \"\"\", (
                    str(uuid.uuid4()),
                    page_url,
                    referrer,
                    user_agent,
                    session_id
                ))
                logger.info(f\"Page view tracked locally (was destined for Plausible): {page_url}\")
        except Exception as e:
            logger.error(f\"Failed to track page view locally: {e}\")
    
    def record_metric(self, metric_name: str, metric_value: float, tags: Dict[str, Any] = None, service_name: str = 'plane'):
        \"\"\"
        Record performance metric locally (replaces OpenTelemetry)
        
        PRIVACY NOTE: Originally would be sent to external OpenTelemetry collector
        Now stored locally in performance_metrics table
        \"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(\"\"\"
                    INSERT INTO performance_metrics (id, metric_name, metric_value, tags, service_name)
                    VALUES (?, ?, ?, ?, ?)
                \"\"\", (
                    str(uuid.uuid4()),
                    metric_name,
                    metric_value,
                    json.dumps(tags or {}),
                    service_name
                ))
                logger.info(f\"Performance metric recorded locally (was destined for OpenTelemetry): {metric_name}\")
        except Exception as e:
            logger.error(f\"Failed to record performance metric locally: {e}\")
    
    def store_plane_telemetry(self, telemetry_type: str, data: Dict[str, Any], instance_id: str = None):
        \"\"\"
        Store Plane telemetry locally (replaces Plane.so telemetry)
        
        PRIVACY NOTE: Originally would be sent to telemetry.plane.so
        Now stored locally in plane_telemetry table
        \"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(\"\"\"
                    INSERT INTO plane_telemetry (id, telemetry_type, data, instance_id)
                    VALUES (?, ?, ?, ?)
                \"\"\", (
                    str(uuid.uuid4()),
                    telemetry_type,
                    json.dumps(data),
                    instance_id
                ))
                logger.info(f\"Plane telemetry stored locally (was destined for Plane.so): {telemetry_type}\")
        except Exception as e:
            logger.error(f\"Failed to store Plane telemetry locally: {e}\")
    
    def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        \"\"\"Get comprehensive analytics data for dashboard display\"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get counts for each service
                services = {
                    'user_events': 'app.posthog.com',
                    'error_logs': 'sentry.io',
                    'session_recordings': 'clarity.microsoft.com', 
                    'page_analytics': 'plausible.io',
                    'performance_metrics': 'opentelemetry-collector',
                    'plane_telemetry': 'telemetry.plane.so'
                }
                
                summary = {}
                for table, destination in services.items():
                    cursor = conn.execute(f\"SELECT COUNT(*) FROM {table}\")
                    count = cursor.fetchone()[0]
                    summary[table] = {
                        'count': count,
                        'original_destination': destination
                    }
                
                return {
                    'summary': summary,
                    'message': 'All analytics data stored locally - Zero external transmission',
                    'privacy_status': 'SECURE - No data exfiltration',
                    'last_updated': datetime.utcnow().isoformat()
                }
        except Exception as e:
            logger.error(f\"Failed to get analytics dashboard data: {e}\")
            return {
                'summary': {},
                'message': f'Analytics data temporarily unavailable: {str(e)}',
                'privacy_status': 'SECURE - No data exfiltration (service error)'
            }
    
    def get_user_events(self, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        \"\"\"Get user events (originally would have been from PostHog)\"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                if user_id:
                    cursor = conn.execute(\"\"\"
                        SELECT * FROM user_events 
                        WHERE user_id = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    \"\"\", (user_id, limit))
                else:
                    cursor = conn.execute(\"\"\"
                        SELECT * FROM user_events 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    \"\"\", (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f\"Failed to get user events: {e}\")
            return []
    
    def get_error_summary(self, days: int = 7) -> Dict[str, Any]:
        \"\"\"Get error summary (originally would have been from Sentry)\"\"\"
        try:
            with sqlite3.connect(self.db_path) as conn:
                since_date = datetime.utcnow() - timedelta(days=days)
                
                # Total errors
                cursor = conn.execute(\"\"\"
                    SELECT COUNT(*) FROM error_logs 
                    WHERE timestamp >= ?
                \"\"\", (since_date.isoformat(),))
                total_errors = cursor.fetchone()[0]
                
                # Error types
                cursor = conn.execute(\"\"\"
                    SELECT error_type, COUNT(*) as count, MAX(timestamp) as last_seen
                    FROM error_logs 
                    WHERE timestamp >= ?
                    GROUP BY error_type
                    ORDER BY count DESC
                    LIMIT 10
                \"\"\", (since_date.isoformat(),))
                
                error_types = []
                for row in cursor.fetchall():
                    error_types.append({
                        'type': row[0],
                        'count': row[1],
                        'last_seen': row[2]
                    })
                
                return {
                    'total_errors': total_errors,
                    'error_types': error_types,
                    'period_days': days
                }
        except Exception as e:
            logger.error(f\"Failed to get error summary: {e}\")
            return {
                'total_errors': 0,
                'error_types': [],
                'error': str(e)
            }

# Global instance
local_analytics = LocalAnalyticsService()
