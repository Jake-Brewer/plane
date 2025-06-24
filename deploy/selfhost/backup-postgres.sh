#!/bin/bash
# Plane PostgreSQL Backup Script with NAS Resilience
# Automated backup with rotation to NAS drive and local fallback
# Usage: ./backup-postgres.sh

set -e

# Configuration
NAS_BACKUP_DIR="Z:/plane-backups/postgres"
LOCAL_BACKUP_DIR="/tmp/plane-backups/postgres"
CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"
RETENTION_DAYS=30
MAX_LOCAL_BACKUPS=7  # Keep max 7 local backups when NAS offline

# Function to check if NAS is available
check_nas_available() {
    if [ -d "Z:/" ] && [ -w "Z:/" ]; then
        return 0  # NAS available
    else
        return 1  # NAS not available
    fi
}

# Function to ensure backup directory exists
ensure_backup_dir() {
    local backup_dir="$1"
    mkdir -p "$backup_dir" 2>/dev/null || {
        echo "Warning: Could not create backup directory: $backup_dir"
        return 1
    }
    return 0
}

# Function to sync pending local backups to NAS when it comes online
sync_local_backups_to_nas() {
    local pending_file="$LOCAL_BACKUP_DIR/pending_nas_sync.txt"
    
    if [ ! -f "$pending_file" ]; then
        return 0  # No pending backups
    fi
    
    echo "🔄 Syncing pending local backups to NAS..."
    ensure_backup_dir "$NAS_BACKUP_DIR"
    
    local sync_count=0
    while IFS= read -r backup_file; do
        local local_path="$LOCAL_BACKUP_DIR/$backup_file"
        local nas_path="$NAS_BACKUP_DIR/$backup_file"
        
        if [ -f "$local_path" ]; then
            if cp "$local_path" "$nas_path" 2>/dev/null; then
                echo "  ✅ Synced: $backup_file"
                sync_count=$((sync_count + 1))
            else
                echo "  ❌ Failed to sync: $backup_file"
            fi
        fi
    done < "$pending_file"
    
    if [ $sync_count -gt 0 ]; then
        echo "📊 Synced $sync_count backup(s) to NAS"
        # Clear the pending list after successful sync
        > "$pending_file"
        
        # Copy the local log to NAS and merge
        if [ -f "$LOCAL_BACKUP_DIR/backup.log" ]; then
            cat "$LOCAL_BACKUP_DIR/backup.log" >> "$NAS_BACKUP_DIR/backup.log"
            > "$LOCAL_BACKUP_DIR/backup.log"
        fi
    fi
}

# Determine backup destination based on NAS availability
if check_nas_available; then
    BACKUP_DIR="$NAS_BACKUP_DIR"
    NAS_ONLINE=true
    echo "✅ NAS available - using primary backup location"
else
    BACKUP_DIR="$LOCAL_BACKUP_DIR"
    NAS_ONLINE=false
    echo "⚠️ NAS offline - using local backup fallback"
fi

# Ensure backup directory exists
if ! ensure_backup_dir "$BACKUP_DIR"; then
    echo "❌ Cannot create backup directory. Backup failed."
    exit 1
fi

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="plane_backup_${TIMESTAMP}.sql"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

echo "Starting PostgreSQL backup at $(date)"
echo "Backup destination: $BACKUP_PATH"

# Create backup using docker exec
docker exec $CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME > "$BACKUP_PATH"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_FILE"
    
    # Compress the backup
    gzip "$BACKUP_PATH"
    echo "Backup compressed: ${BACKUP_FILE}.gz"
    
    if [ "$NAS_ONLINE" = true ]; then
        # NAS is online - normal retention
        find "$BACKUP_DIR" -name "plane_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
        echo "Old backups cleaned up (older than $RETENTION_DAYS days)"
        
        # Try to sync any pending local backups to NAS
        sync_local_backups_to_nas
        
        # Log success
        echo "$(date): Backup successful (NAS) - ${BACKUP_FILE}.gz" >> "$BACKUP_DIR/backup.log"
    else
        # NAS is offline - limited local retention
        find "$BACKUP_DIR" -name "plane_backup_*.sql.gz" | sort -r | tail -n +$((MAX_LOCAL_BACKUPS + 1)) | xargs -r rm
        echo "Local backup retention applied (keeping $MAX_LOCAL_BACKUPS backups)"
        
        # Log to local file and mark for later NAS sync
        echo "$(date): Backup successful (LOCAL) - ${BACKUP_FILE}.gz" >> "$BACKUP_DIR/backup.log"
        echo "${BACKUP_FILE}.gz" >> "$BACKUP_DIR/pending_nas_sync.txt"
        echo "⚠️ Backup queued for NAS sync when available"
    fi
else
    echo "Backup failed!"
    if [ "$NAS_ONLINE" = true ]; then
        echo "$(date): Backup failed" >> "$BACKUP_DIR/backup.log"
    else
        echo "$(date): Backup failed" >> "$LOCAL_BACKUP_DIR/backup.log"
    fi
    exit 1
fi

echo "Backup process completed at $(date)" 