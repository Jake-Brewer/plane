#!/bin/bash
# Plane Data Export Script
# Exports all project management data for backup/migration
# Usage: ./export-data.sh

set -e

EXPORT_DIR="Z:/plane-backups/exports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
EXPORT_PATH="$EXPORT_DIR/plane_export_$TIMESTAMP"
CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"

echo "Starting Plane data export at $(date)"
mkdir -p "$EXPORT_PATH"

# 1. Database Export (Full SQL dump)
echo "📊 Exporting database..."
docker exec $CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME > "$EXPORT_PATH/database_full.sql"

# 2. Database Export (JSON format for each table)
echo "📄 Exporting database tables as JSON..."
mkdir -p "$EXPORT_PATH/json"

# Key tables to export individually
TABLES=(
    "plane_workspace"
    "plane_project" 
    "plane_issue"
    "plane_user"
    "plane_projectmember"
    "plane_workspacemember"
    "plane_cycle"
    "plane_module"
    "plane_page"
    "plane_apitoken"
)

for table in "${TABLES[@]}"; do
    echo "  Exporting $table..."
    docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "COPY (SELECT * FROM $table) TO STDOUT WITH CSV HEADER;" > "$EXPORT_PATH/json/${table}.csv" 2>/dev/null || echo "    Warning: Table $table might not exist"
done

# 3. File Uploads Export
echo "📁 Exporting file uploads..."
if [ -d "Z:/plane-data/uploads" ]; then
    cp -r "Z:/plane-data/uploads" "$EXPORT_PATH/uploads"
    echo "  Uploads exported: $(du -sh "$EXPORT_PATH/uploads" | cut -f1)"
else
    echo "  No uploads directory found"
fi

# 4. Configuration Export
echo "⚙️ Exporting configuration..."
mkdir -p "$EXPORT_PATH/config"
cp deploy/selfhost/variables.env "$EXPORT_PATH/config/" 2>/dev/null || echo "  Warning: variables.env not found"
cp deploy/selfhost/docker-compose.yml "$EXPORT_PATH/config/" 2>/dev/null || echo "  Warning: docker-compose.yml not found"

# 5. Create export manifest
echo "📋 Creating export manifest..."
cat > "$EXPORT_PATH/EXPORT_MANIFEST.txt" << EOF
Plane Data Export Manifest
=========================
Export Date: $(date)
Export Path: $EXPORT_PATH

Contents:
- database_full.sql: Complete PostgreSQL database dump
- json/: Individual table exports in CSV format
- uploads/: All uploaded files and attachments
- config/: Configuration files (docker-compose.yml, variables.env)

Restoration:
1. Restore database: ../restore-postgres.sh database_full.sql
2. Copy uploads to Z:/plane-data/uploads/
3. Update configuration files as needed

Tables Exported:
$(for table in "${TABLES[@]}"; do echo "  - $table"; done)

Export Size: $(du -sh "$EXPORT_PATH" | cut -f1)
EOF

# 6. Compress the export
echo "🗜️ Compressing export..."
cd "$EXPORT_DIR"
tar -czf "plane_export_$TIMESTAMP.tar.gz" "plane_export_$TIMESTAMP/"

if [ $? -eq 0 ]; then
    echo "✅ Export completed successfully!"
    echo "   Archive: $EXPORT_DIR/plane_export_$TIMESTAMP.tar.gz"
    echo "   Size: $(du -sh "$EXPORT_DIR/plane_export_$TIMESTAMP.tar.gz" | cut -f1)"
    
    # Clean up uncompressed directory
    rm -rf "$EXPORT_PATH"
    
    echo "$(date): Export successful - plane_export_$TIMESTAMP.tar.gz" >> "$EXPORT_DIR/export.log"
else
    echo "❌ Export compression failed"
    echo "$(date): Export compression failed" >> "$EXPORT_DIR/export.log"
    exit 1
fi

echo "Export process completed at $(date)" 