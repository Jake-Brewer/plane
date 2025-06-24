#!/bin/bash
# Plane NAS Directory Setup Script
# Creates required directories on NAS before deployment
# Usage: ./setup-nas-directories.sh

set -e

echo "Setting up Plane NAS directories..."

# Base directories
NAS_BASE="Z:/plane-data"
BACKUP_BASE="Z:/plane-backups"

# Create data directories
mkdir -p "$NAS_BASE/postgres"
mkdir -p "$NAS_BASE/redis"
mkdir -p "$NAS_BASE/uploads"
mkdir -p "$NAS_BASE/rabbitmq"
mkdir -p "$NAS_BASE/logs/api"
mkdir -p "$NAS_BASE/logs/worker"
mkdir -p "$NAS_BASE/logs/beat-worker"
mkdir -p "$NAS_BASE/logs/migrator"

# Create backup directories
mkdir -p "$BACKUP_BASE/postgres"

# Set appropriate permissions (if on Linux/WSL)
if command -v chmod >/dev/null 2>&1; then
    echo "Setting directory permissions..."
    chmod -R 755 "$NAS_BASE"
    chmod -R 755 "$BACKUP_BASE"
fi

echo "✅ NAS directories created successfully:"
echo "   Data: $NAS_BASE"
echo "   Backups: $BACKUP_BASE"
echo ""
echo "Directory structure:"
find "$NAS_BASE" -type d 2>/dev/null || echo "   (Use Windows Explorer to verify Z:/plane-data structure)"
echo ""
echo "🚀 Ready for deployment! Run: docker-compose -f deploy/selfhost/docker-compose.yml up -d" 