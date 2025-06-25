#!/usr/bin/env python3
"""
Traffic Interceptor for Plane Security
Intercepts HTTP/HTTPS traffic and blocks external data exfiltration
"""

import os
import sys
import json
import time
import logging
import socket
import threading
import ssl
import sqlite3
from datetime import datetime
from typing import Dict, List, Any
from urllib.parse import urlparse
import subprocess
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - INTERCEPTOR - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/plane-traffic.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TrafficInterceptor:
    """
    Intercepts and analyzes network traffic for data exfiltration attempts
    """
    
    def __init__(self):
        self.db_path = '/var/log/plane-security.db'
        self.blocked_domains = {
            'telemetry.plane.so',
            'app.plane.so',
            'posthog.com',
            'mixpanel.com',
            'segment.com',
            'amplitude.com'
        }
        self.proxy_port = 8888
        self.ssl_proxy_port = 8443
        self.running = True
        
    def log_blocked_traffic(self, method: str, url: str, headers: Dict, payload: str = None):
        """Log blocked traffic attempt"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocked_traffic (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    method TEXT NOT NULL,
                    url TEXT NOT NULL,
                    headers TEXT,
                    payload_size INTEGER,
                    payload_preview TEXT,
                    severity TEXT DEFAULT 'CRITICAL'
                )
            ''')
            
            payload_size = len(payload) if payload else 0
            payload_preview = payload[:1000] if payload else None
            
            cursor.execute('''
                INSERT INTO blocked_traffic
                (timestamp, method, url, headers, payload_size, payload_preview)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                method,
                url,
                json.dumps(headers),
                payload_size,
                payload_preview
            ))
            
            conn.commit()
            conn.close()
            
            logger.critical(f"BLOCKED: {method} {url} ({payload_size} bytes)")
            
        except Exception as e:
            logger.error(f"Failed to log blocked traffic: {e}")
    
    def is_blocked_domain(self, hostname: str) -> bool:
        """Check if hostname should be blocked"""
        return any(blocked in hostname for blocked in self.blocked_domains)
    
    def handle_request(self, client_socket, client_addr):
        """Handle individual requests"""
        try:
            request_data = client_socket.recv(8192).decode('utf-8', errors='ignore')
            
            if not request_data:
                client_socket.close()
                return
            
            lines = request_data.split('\r\n')
            if not lines:
                client_socket.close()
                return
            
            try:
                method, url, protocol = lines[0].split(' ', 2)
            except ValueError:
                client_socket.close()
                return
            
            headers = {}
            for line in lines[1:]:
                if line == '':
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()
            
            hostname = headers.get('host', '')
            if not hostname and url.startswith('http'):
                hostname = urlparse(url).hostname
            
            if self.is_blocked_domain(hostname):
                self.log_blocked_traffic(method, url, headers, request_data)
                
                response = (
                    "HTTP/1.1 403 Forbidden\r\n"
                    "Content-Type: text/html\r\n"
                    "Content-Length: 100\r\n"
                    "\r\n"
                    "<h1>403 Forbidden</h1><p>Data exfiltration blocked by Plane Security Monitor</p>"
                )
                client_socket.send(response.encode())
            
            client_socket.close()
            
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            try:
                client_socket.close()
            except:
                pass
    
    def start_proxy(self):
        """Start HTTP proxy server"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', self.proxy_port))
            server_socket.listen(10)
            
            logger.info(f"Traffic interceptor listening on port {self.proxy_port}")
            
            while self.running:
                try:
                    client_socket, client_addr = server_socket.accept()
                    thread = threading.Thread(
                        target=self.handle_request,
                        args=(client_socket, client_addr)
                    )
                    thread.daemon = True
                    thread.start()
                except Exception as e:
                    if self.running:
                        logger.error(f"Error accepting connection: {e}")
            
            server_socket.close()
            
        except Exception as e:
            logger.error(f"Proxy error: {e}")
    
    def setup_iptables_redirect(self):
        """Setup iptables to redirect traffic to our proxy"""
        try:
            # Redirect HTTP traffic to our proxy
            subprocess.run([
                'iptables', '-t', 'nat', '-A', 'OUTPUT',
                '-p', 'tcp', '--dport', '80',
                '!', '-d', '127.0.0.0/8',
                '-j', 'REDIRECT', '--to-port', str(self.proxy_port)
            ], check=True)
            
            # Redirect HTTPS traffic to our SSL proxy  
            subprocess.run([
                'iptables', '-t', 'nat', '-A', 'OUTPUT',
                '-p', 'tcp', '--dport', '443', 
                '!', '-d', '127.0.0.0/8',
                '-j', 'REDIRECT', '--to-port', str(self.ssl_proxy_port)
            ], check=True)
            
            logger.info("TRAFFIC: iptables redirection rules configured")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"TRAFFIC: Failed to setup iptables: {e}")
        except Exception as e:
            logger.error(f"TRAFFIC: Error setting up iptables: {e}")
    
    def start_monitoring(self):
        """Start traffic monitoring"""
        logger.info("Starting Traffic Interceptor")
        
        proxy_thread = threading.Thread(target=self.start_proxy)
        proxy_thread.daemon = True
        proxy_thread.start()
        
        # Setup iptables redirection (if running with privileges)
        try:
            self.setup_iptables_redirect()
        except Exception as e:
            logger.warning(f"TRAFFIC: Could not setup iptables (may need privileges): {e}")
        
        logger.info("TRAFFIC: Traffic interceptor active")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(60)
                logger.info("Traffic interceptor running")
        except KeyboardInterrupt:
            logger.info("Stopping interceptor")
            self.running = False


def main():
    """Main function"""
    interceptor = TrafficInterceptor()
    interceptor.start_monitoring()


if __name__ == "__main__":
    main() 