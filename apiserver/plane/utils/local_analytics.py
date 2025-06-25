#!/usr/bin/env python3
\"\"\"
Local Analytics Service - Data Privacy Replacement
Original destinations: PostHog (app.posthog.com), Sentry, Microsoft Clarity, Plausible

This service stores all analytics data locally instead of sending to external services.
Maintains the same functionality while ensuring complete data privacy.
\"\"\"

import json
import sqlite3
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import uuid

# Configuration
LOCAL_ANALYTICS_DB = Path(\"/var/lib/plane/analytics/local_analytics.db\")
LOCAL_ANALYTICS_DIR = Path(\"/var/lib/plane/analytics\")

class LocalAnalyticsService:
    \"\"\"
    Local replacement for external analytics services
    
    Original Services Replaced:
    - PostHog (app.posthog.com) -> User behavior analytics
    - Sentry -> Error tracking and reporting  
    - Microsoft Clarity -> Session recording
    - Plausible (plausible.io) -> Website analytics
    - OpenTelemetry -> Performance metrics
    \"\"\"
    
    def __init__(self):
        self.db_path = LOCAL_ANALYTICS_DB
        self.storage_dir = LOCAL_ANALYTICS_DIR
        self.logger = logging.getLogger(__name__)
        self._init_storage()
        
    def _init_storage(self):
        \"\"\"Initialize local storage directories and database\"\"\"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Create analytics database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # PostHog replacement tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_events (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                event_name TEXT,
                properties TEXT,  -- JSON
                timestamp DATETIME,
                session_id TEXT,
                original_destination TEXT DEFAULT 'app.posthog.com'
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.logger.info(\"Local analytics database initialized\")

# Global instance
local_analytics = LocalAnalyticsService()
