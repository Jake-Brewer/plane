#!/bin/bash
# Plane NAS Availability Monitor
# Monitors NAS availability and triggers sync when it comes back online
# Usage: ./monitor-nas.sh [--daemon] [--interval=60]

# Configuration
NAS_PATH="Z:/"
CHECK_INTERVAL=60  # seconds
LOG_FILE="/tmp/plane-nas-monitor.log"
SYNC_SCRIPT="./sync-nas-backups.sh"
DAEMON_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --daemon)
            DAEMON_MODE=true
            shift
            ;;
        --interval=*)
            CHECK_INTERVAL="${1#*=}"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--daemon] [--interval=60]"
            echo "  --daemon    Run in background as daemon"
            echo "  --interval  Check interval in seconds (default: 60)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Function to log messages
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Function to check if NAS is available
check_nas_available() {
    if [ -d "$NAS_PATH" ] && [ -w "$NAS_PATH" ]; then
        return 0  # Available
    else
        return 1  # Not available
    fi
}

# Function to send notification (placeholder - can be extended)
send_notification() {
    local message="$1"
    local level="$2"  # INFO, WARNING, ERROR
    
    log_message "[$level] $message"
    
    # Future: Add email, Slack, or other notifications here
    # echo "$message" | mail -s "Plane NAS Alert" admin@example.com
}

# Function to trigger backup sync
trigger_sync() {
    log_message "Triggering backup sync to NAS..."
    
    if [ -f "$SYNC_SCRIPT" ] && [ -x "$SYNC_SCRIPT" ]; then
        if "$SYNC_SCRIPT" >> "$LOG_FILE" 2>&1; then
            send_notification "Backup sync completed successfully" "INFO"
            return 0
        else
            send_notification "Backup sync failed - check logs" "ERROR"
            return 1
        fi
    else
        send_notification "Sync script not found or not executable: $SYNC_SCRIPT" "ERROR"
        return 1
    fi
}

# Function to run single check
run_single_check() {
    if check_nas_available; then
        echo "✅ NAS is available"
        
        # Check if there are pending backups to sync
        local pending_file="/tmp/plane-backups/postgres/pending_nas_sync.txt"
        if [ -f "$pending_file" ] && [ -s "$pending_file" ]; then
            echo "🔄 Found pending backups - triggering sync..."
            trigger_sync
        else
            echo "ℹ️ No pending backups to sync"
        fi
    else
        echo "❌ NAS is not available"
    fi
}

# Function to run daemon mode
run_daemon() {
    local nas_was_offline=false
    
    log_message "Starting NAS monitor daemon (check interval: ${CHECK_INTERVAL}s)"
    send_notification "NAS monitor daemon started" "INFO"
    
    while true; do
        if check_nas_available; then
            if [ "$nas_was_offline" = true ]; then
                # NAS just came back online
                send_notification "NAS is back online!" "INFO"
                
                # Wait a moment for NAS to stabilize
                sleep 5
                
                # Trigger sync
                trigger_sync
                
                nas_was_offline=false
            fi
        else
            if [ "$nas_was_offline" = false ]; then
                # NAS just went offline
                send_notification "NAS has gone offline - backups will use local storage" "WARNING"
                nas_was_offline=true
            fi
        fi
        
        sleep "$CHECK_INTERVAL"
    done
}

# Function to check if daemon is already running
check_daemon_running() {
    local pid_file="/tmp/plane-nas-monitor.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # Running
        else
            rm -f "$pid_file"  # Stale PID file
            return 1  # Not running
        fi
    else
        return 1  # Not running
    fi
}

# Function to start daemon
start_daemon() {
    local pid_file="/tmp/plane-nas-monitor.pid"
    
    if check_daemon_running; then
        echo "❌ NAS monitor daemon is already running (PID: $(cat $pid_file))"
        exit 1
    fi
    
    echo "🚀 Starting NAS monitor daemon..."
    
    # Start daemon in background
    (
        echo $$ > "$pid_file"
        run_daemon
    ) &
    
    local daemon_pid=$!
    echo "✅ NAS monitor daemon started (PID: $daemon_pid)"
    echo "📝 Logs: $LOG_FILE"
    echo "🛑 To stop: kill $daemon_pid"
}

# Function to stop daemon
stop_daemon() {
    local pid_file="/tmp/plane-nas-monitor.pid"
    
    if check_daemon_running; then
        local pid=$(cat "$pid_file")
        echo "🛑 Stopping NAS monitor daemon (PID: $pid)..."
        kill "$pid"
        rm -f "$pid_file"
        echo "✅ Daemon stopped"
    else
        echo "ℹ️ No daemon running"
    fi
}

# Main execution
echo "🔍 Plane NAS Availability Monitor"
echo "================================="

# Handle special commands
case "${1:-}" in
    stop)
        stop_daemon
        exit 0
        ;;
    status)
        if check_daemon_running; then
            echo "✅ Daemon is running (PID: $(cat /tmp/plane-nas-monitor.pid))"
        else
            echo "❌ Daemon is not running"
        fi
        exit 0
        ;;
esac

if [ "$DAEMON_MODE" = true ]; then
    start_daemon
else
    run_single_check
fi 