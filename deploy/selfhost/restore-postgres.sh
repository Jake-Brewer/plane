#!/bin/bash
# Plane PostgreSQL Restore Script
# Restore from backup file
# Usage: ./restore-postgres.sh <backup_file.sql.gz>

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file.sql.gz>"
    echo "Available backups:"
    ls -la Z:/plane-backups/postgres/plane_backup_*.sql.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"
CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' not found"
    exit 1
fi

echo "WARNING: This will overwrite the current database!"
echo "Backup file: $BACKUP_FILE"
echo "Target database: $DB_NAME"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo "Starting restore at $(date)"

# Extract the backup if it's compressed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "Extracting compressed backup..."
    TEMP_FILE="/tmp/plane_restore_temp.sql"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    RESTORE_FILE="$TEMP_FILE"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Stop the application containers to prevent connections
echo "Stopping application containers..."
docker-compose -f deploy/selfhost/docker-compose.yml stop web space admin api worker beat-worker

# Drop and recreate database
echo "Recreating database..."
docker exec $CONTAINER_NAME psql -U $DB_USER -c "DROP DATABASE IF EXISTS $DB_NAME;"
docker exec $CONTAINER_NAME psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;"

# Restore the backup
echo "Restoring backup..."
docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME < "$RESTORE_FILE"

if [ $? -eq 0 ]; then
    echo "Restore completed successfully!"
    
    # Clean up temp file if created
    if [ -f "$TEMP_FILE" ]; then
        rm "$TEMP_FILE"
    fi
    
    # Restart application containers
    echo "Restarting application containers..."
    docker-compose -f deploy/selfhost/docker-compose.yml up -d
    
    echo "$(date): Restore successful from $BACKUP_FILE" >> "Z:/plane-backups/postgres/restore.log"
else
    echo "Restore failed!"
    echo "$(date): Restore failed from $BACKUP_FILE" >> "Z:/plane-backups/postgres/restore.log"
    exit 1
fi

echo "Restore process completed at $(date)" 