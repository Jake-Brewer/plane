#!/bin/bash
# Plane PostgreSQL Backup Script
# Automated backup with rotation to NAS drive
# Usage: ./backup-postgres.sh

set -e

# Configuration
BACKUP_DIR="Z:/plane-backups/postgres"
CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

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
    
    # Remove old backups (older than retention period)
    find "$BACKUP_DIR" -name "plane_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "Old backups cleaned up (older than $RETENTION_DAYS days)"
    
    # Log success
    echo "$(date): Backup successful - ${BACKUP_FILE}.gz" >> "$BACKUP_DIR/backup.log"
else
    echo "Backup failed!"
    echo "$(date): Backup failed" >> "$BACKUP_DIR/backup.log"
    exit 1
fi

echo "Backup process completed at $(date)" 