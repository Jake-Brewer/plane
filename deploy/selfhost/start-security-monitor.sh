#!/bin/bash

echo "🔒 Starting Plane Security Monitor"
echo "=================================="

# Create log directory
mkdir -p /var/log
chmod 755 /var/log

# Initialize security database
echo "📊 Initializing security database..."
python3 -c "
import sqlite3
import os

db_path = '/var/log/plane-security.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
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

conn.commit()
conn.close()
print('Security database initialized')
"

# Setup iptables rules (if running with privileges)
echo "🛡️  Setting up network security rules..."
if [ "$(id -u)" = "0" ]; then
    echo "Running as root - configuring iptables..."
    
    # Create custom chain
    iptables -t filter -N PLANE_SECURITY 2>/dev/null || true
    
    # Log external HTTPS connections
    iptables -A OUTPUT -p tcp --dport 443 ! -d 127.0.0.0/8 ! -d 10.0.0.0/8 ! -d 172.16.0.0/12 ! -d 192.168.0.0/16 -j LOG --log-prefix "PLANE_HTTPS_OUT: " 2>/dev/null || true
    
    # Log external HTTP connections  
    iptables -A OUTPUT -p tcp --dport 80 ! -d 127.0.0.0/8 ! -d 10.0.0.0/8 ! -d 172.16.0.0/12 ! -d 192.168.0.0/16 -j LOG --log-prefix "PLANE_HTTP_OUT: " 2>/dev/null || true
    
    echo "iptables rules configured"
else
    echo "Not running as root - skipping iptables configuration"
fi

# Start traffic interceptor in background
echo "🚦 Starting traffic interceptor..."
python3 /app/traffic-interceptor.py &
INTERCEPTOR_PID=$!

# Start network monitor in background  
echo "📡 Starting network monitor..."
python3 /app/network-monitor.py &
MONITOR_PID=$!

echo "✅ Plane Security Monitor started successfully"
echo "📊 Security dashboard will be available on port 8889"
echo "🚦 Traffic interceptor listening on port 8888"
echo "📝 Logs available in /var/log/plane-security.log"

# Function to handle shutdown
shutdown_handler() {
    echo "🛑 Shutting down Plane Security Monitor..."
    kill $INTERCEPTOR_PID 2>/dev/null || true
    kill $MONITOR_PID 2>/dev/null || true
    echo "✅ Security monitor stopped"
    exit 0
}

# Set up signal handlers
trap shutdown_handler SIGTERM SIGINT

# Keep container running and monitor processes
while true; do
    # Check if processes are still running
    if ! kill -0 $INTERCEPTOR_PID 2>/dev/null; then
        echo "⚠️  Traffic interceptor stopped, restarting..."
        python3 /app/traffic-interceptor.py &
        INTERCEPTOR_PID=$!
    fi
    
    if ! kill -0 $MONITOR_PID 2>/dev/null; then
        echo "⚠️  Network monitor stopped, restarting..."
        python3 /app/network-monitor.py &
        MONITOR_PID=$!
    fi
    
    # Log status every 5 minutes
    echo "🔒 Security monitor active - $(date)"
    
    sleep 300  # 5 minutes
done 