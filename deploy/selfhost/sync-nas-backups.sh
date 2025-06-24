#!/bin/bash
# Plane NAS Backup Sync Script
# Syncs local backups to NAS when it comes back online
# Usage: ./sync-nas-backups.sh

set -e

# Configuration
NAS_BACKUP_DIR="Z:/plane-backups/postgres"
LOCAL_BACKUP_DIR="/tmp/plane-backups/postgres"
NAS_DATA_DIR="Z:/plane-data"

# Function to check if NAS is available
check_nas_available() {
    if [ -d "Z:/" ] && [ -w "Z:/" ]; then
        return 0  # NAS available
    else
        return 1  # NAS not available
    fi
}

# Function to sync all local backups to NAS
sync_all_backups() {
    echo "🔄 Syncing all local backups to NAS..."
    
    if [ ! -d "$LOCAL_BACKUP_DIR" ]; then
        echo "No local backup directory found"
        return 0
    fi
    
    mkdir -p "$NAS_BACKUP_DIR"
    local sync_count=0
    local skip_count=0
    
    # Sync all backup files
    for local_backup in "$LOCAL_BACKUP_DIR"/plane_backup_*.sql.gz; do
        if [ -f "$local_backup" ]; then
            local backup_name=$(basename "$local_backup")
            local nas_backup="$NAS_BACKUP_DIR/$backup_name"
            
            if [ ! -f "$nas_backup" ]; then
                if cp "$local_backup" "$nas_backup"; then
                    echo "  ✅ Synced: $backup_name"
                    sync_count=$((sync_count + 1))
                else
                    echo "  ❌ Failed to sync: $backup_name"
                fi
            else
                echo "  ⏭️ Skipped (exists): $backup_name"
                skip_count=$((skip_count + 1))
            fi
        fi
    done
    
    echo "📊 Sync complete: $sync_count new, $skip_count skipped"
    return $sync_count
}

# Function to merge log files
merge_log_files() {
    local local_log="$LOCAL_BACKUP_DIR/backup.log"
    local nas_log="$NAS_BACKUP_DIR/backup.log"
    
    if [ -f "$local_log" ]; then
        echo "📝 Merging backup logs..."
        cat "$local_log" >> "$nas_log"
        > "$local_log"  # Clear local log after merge
        echo "✅ Log files merged"
    fi
}

# Function to clean up old local backups after sync
cleanup_local_backups() {
    local keep_count=${1:-3}  # Keep 3 most recent by default
    
    echo "🧹 Cleaning up old local backups (keeping $keep_count most recent)..."
    
    local backup_count=$(find "$LOCAL_BACKUP_DIR" -name "plane_backup_*.sql.gz" | wc -l)
    
    if [ "$backup_count" -gt "$keep_count" ]; then
        find "$LOCAL_BACKUP_DIR" -name "plane_backup_*.sql.gz" | sort -r | tail -n +$((keep_count + 1)) | xargs -r rm
        echo "✅ Cleaned up $((backup_count - keep_count)) old local backups"
    else
        echo "ℹ️ Only $backup_count local backups found, no cleanup needed"
    fi
}

# Function to check NAS health
check_nas_health() {
    echo "🏥 Checking NAS health..."
    
    # Check if we can write to NAS
    local test_file="Z:/plane-data/.nas_health_check"
    if echo "$(date)" > "$test_file" 2>/dev/null; then
        rm -f "$test_file"
        echo "✅ NAS write test successful"
        return 0
    else
        echo "❌ NAS write test failed"
        return 1
    fi
}

# Main execution
echo "🔗 Plane NAS Backup Sync Tool"
echo "=============================="

# Check if NAS is available
if ! check_nas_available; then
    echo "❌ NAS is not available (Z: drive not accessible)"
    echo "   Please ensure NAS is online and mounted before running this script"
    exit 1
fi

echo "✅ NAS is available"

# Check NAS health
if ! check_nas_health; then
    echo "⚠️ NAS health check failed - proceeding with caution"
fi

# Sync backups
if sync_all_backups; then
    synced_count=$?
    
    # Merge logs
    merge_log_files
    
    # Clear pending sync list if it exists
    local pending_file="$LOCAL_BACKUP_DIR/pending_nas_sync.txt"
    if [ -f "$pending_file" ]; then
        > "$pending_file"
        echo "✅ Cleared pending sync list"
    fi
    
    # Cleanup old local backups (keep 3 most recent)
    cleanup_local_backups 3
    
    echo ""
    echo "🎉 NAS sync completed successfully!"
    echo "   - Synced $synced_count backup files to NAS"
    echo "   - Merged backup logs"
    echo "   - Cleaned up old local backups"
    echo ""
    echo "💡 Your backup system is now fully synchronized"
else
    echo "❌ NAS sync encountered errors"
    exit 1
fi 