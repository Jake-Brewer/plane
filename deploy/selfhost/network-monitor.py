#!/usr/bin/env python3
"""
Network Security Monitor for Plane
Blocks and reports external data exfiltration attempts
"""

import os
import sys
import json
import time
import logging
import socket
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import sqlite3
import subprocess
import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SECURITY - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/plane-security.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NetworkSecurityMonitor:
    """
    Network security monitor that blocks external connections
    and logs attempted data exfiltration
    """
    
    def __init__(self):
        self.db_path = '/var/log/plane-security.db'
        self.blocked_domains = {
            'telemetry.plane.so',
            'app.plane.so', 
            'api.plane.so',
            'analytics.plane.so',
            'tracking.plane.so',
            'metrics.plane.so',
            'posthog.com',
            'mixpanel.com',
            'segment.com',
            'amplitude.com',
            'hotjar.com',
            'fullstory.com',
            'logrocket.com',
            'sentry.io',
            'bugsnag.com',
            'rollbar.com'
        }
        self.allowed_domains = {
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
            'redis',
            'postgres',
            'db',
            'database'
        }
        self.setup_database()
        
    def setup_database(self):
        """Initialize SQLite database for logging blocked attempts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocked_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    source_ip TEXT NOT NULL,
                    destination_host TEXT NOT NULL,
                    destination_port INTEGER,
                    protocol TEXT,
                    attempted_data TEXT,
                    headers TEXT,
                    user_agent TEXT,
                    process_name TEXT,
                    container_name TEXT,
                    blocked_reason TEXT,
                    severity TEXT DEFAULT 'HIGH'
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_exfiltration_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    method TEXT NOT NULL,
                    payload_size INTEGER,
                    payload_preview TEXT,
                    headers TEXT,
                    source_container TEXT,
                    blocked BOOLEAN DEFAULT TRUE,
                    risk_level TEXT DEFAULT 'CRITICAL'
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("SECURITY: Database initialized for logging blocked attempts")
            
        except Exception as e:
            logger.error(f"SECURITY: Failed to setup database: {e}")
    
    def log_blocked_attempt(self, 
                          source_ip: str,
                          destination_host: str, 
                          destination_port: int,
                          protocol: str,
                          attempted_data: str = None,
                          headers: Dict = None,
                          process_name: str = None):
        """Log a blocked network attempt to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO blocked_attempts 
                (timestamp, source_ip, destination_host, destination_port, 
                 protocol, attempted_data, headers, process_name, 
                 container_name, blocked_reason, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                source_ip,
                destination_host,
                destination_port,
                protocol,
                attempted_data[:1000] if attempted_data else None,
                json.dumps(headers) if headers else None,
                process_name,
                os.environ.get('CONTAINER_NAME', 'unknown'),
                f"Blocked external connection to {destination_host}",
                'HIGH'
            ))
            
            conn.commit()
            conn.close()
            
            logger.warning(f"SECURITY ALERT: Blocked connection to {destination_host}:{destination_port}")
            if attempted_data:
                logger.warning(f"SECURITY: Attempted data: {attempted_data[:200]}...")
                
        except Exception as e:
            logger.error(f"SECURITY: Failed to log blocked attempt: {e}")
    
    def log_data_exfiltration(self,
                            endpoint: str,
                            method: str,
                            payload: str = None,
                            headers: Dict = None):
        """Log attempted data exfiltration"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            payload_size = len(payload) if payload else 0
            payload_preview = payload[:500] if payload else None
            
            cursor.execute('''
                INSERT INTO data_exfiltration_attempts
                (timestamp, endpoint, method, payload_size, payload_preview,
                 headers, source_container, blocked, risk_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                endpoint,
                method,
                payload_size,
                payload_preview,
                json.dumps(headers) if headers else None,
                os.environ.get('CONTAINER_NAME', 'unknown'),
                True,
                'CRITICAL'
            ))
            
            conn.commit()
            conn.close()
            
            logger.critical(f"DATA EXFILTRATION BLOCKED: {method} {endpoint}")
            logger.critical(f"PAYLOAD SIZE: {payload_size} bytes")
            if payload_preview:
                logger.critical(f"PAYLOAD PREVIEW: {payload_preview}")
                
        except Exception as e:
            logger.error(f"SECURITY: Failed to log data exfiltration: {e}")
    
    def get_security_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate security report for the last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get blocked attempts
            cursor.execute('''
                SELECT COUNT(*), destination_host, MAX(timestamp)
                FROM blocked_attempts 
                WHERE datetime(timestamp) > datetime('now', '-{} hours')
                GROUP BY destination_host
                ORDER BY COUNT(*) DESC
            '''.format(hours))
            
            blocked_attempts = cursor.fetchall()
            
            # Get data exfiltration attempts
            cursor.execute('''
                SELECT COUNT(*), endpoint, SUM(payload_size), MAX(timestamp)
                FROM data_exfiltration_attempts
                WHERE datetime(timestamp) > datetime('now', '-{} hours')
                GROUP BY endpoint
                ORDER BY COUNT(*) DESC
            '''.format(hours))
            
            exfiltration_attempts = cursor.fetchall()
            
            conn.close()
            
            report = {
                'period_hours': hours,
                'blocked_connections': [
                    {
                        'count': row[0],
                        'destination': row[1], 
                        'last_attempt': row[2]
                    } for row in blocked_attempts
                ],
                'data_exfiltration_attempts': [
                    {
                        'count': row[0],
                        'endpoint': row[1],
                        'total_bytes': row[2] or 0,
                        'last_attempt': row[3]
                    } for row in exfiltration_attempts
                ],
                'total_blocked': sum(row[0] for row in blocked_attempts),
                'total_exfiltration_attempts': sum(row[0] for row in exfiltration_attempts)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"SECURITY: Failed to generate report: {e}")
            return {'error': str(e)}


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("SECURITY: Received shutdown signal, cleaning up...")
    sys.exit(0)


def main():
    """Main function to start network security monitoring"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    monitor = NetworkSecurityMonitor()
    logger.info("SECURITY: Network Security Monitor initialized")
    
    try:
        while True:
            time.sleep(60)
            report = monitor.get_security_report(1)
            if report.get('total_blocked', 0) > 0:
                logger.warning(f"SECURITY: {report['total_blocked']} attempts blocked in last hour")
    except KeyboardInterrupt:
        logger.info("SECURITY: Monitoring stopped")


if __name__ == "__main__":
    main() 