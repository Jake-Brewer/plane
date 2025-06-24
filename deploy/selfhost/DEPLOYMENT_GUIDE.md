# Plane Secure Local Deployment Guide

## Overview
This guide covers secure deployment of Plane for local use with multi-agent LLM access, including data protection, backup strategies, and security hardening.

## Prerequisites
- Docker and Docker Compose installed
- NAS drive mounted at Z: (RAID 5 recommended)
- Windows/Linux environment with bash support

## Security Features Implemented
✅ **Data Protection**: NAS-based persistent storage with RAID protection  
✅ **Backup Strategy**: Automated PostgreSQL backups with 30-day retention  
✅ **Secure Credentials**: All default passwords replaced with strong credentials  
✅ **CORS Protection**: Limited to localhost access only  
✅ **Connection Limits**: PostgreSQL optimized for local deployment (50 connections)  
✅ **Vulnerability Scanning**: Automated security scanning capabilities  
✅ **Data Export**: Complete data export functionality for portability  

## Deployment Steps

### 1. Pre-Deployment Setup
```bash
# Create NAS directory structure
./setup-nas-directories.sh

# Verify NAS directories exist
ls -la Z:/plane-data/
ls -la Z:/plane-backups/
```

### 2. Configuration Review
Review and customize `variables.env`:
```bash
# Database credentials (already secure)
POSTGRES_USER=plane_admin
POSTGRES_PASSWORD=PlaneDB_Secure_2025!

# RabbitMQ credentials (already secure)  
RABBITMQ_USER=plane_mq_admin
RABBITMQ_PASSWORD=PlaneMQ_Secure_2025!

# MinIO/S3 credentials (already secure)
AWS_ACCESS_KEY_ID=plane_s3_admin
AWS_SECRET_ACCESS_KEY=PlaneS3_Secure_2025!

# CORS protection (already configured)
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://localhost:80,http://127.0.0.1:80
```

### 3. Initial Deployment
```bash
# Deploy all services
docker-compose -f docker-compose.yml up -d

# Check service status
docker-compose -f docker-compose.yml ps

# View logs
docker-compose -f docker-compose.yml logs -f
```

### 4. Post-Deployment Verification
```bash
# Test database connection
docker exec plane-db psql -U plane_admin -d plane -c "SELECT version();"

# Verify data persistence
ls -la Z:/plane-data/postgres/

# Test backup functionality
./backup-postgres.sh

# Verify backup created
ls -la Z:/plane-backups/postgres/
```

## Maintenance Operations

### Daily Backups
Set up automated daily backups:
```bash
# Add to crontab (Linux/WSL) or Task Scheduler (Windows)
0 2 * * * /path/to/backup-postgres.sh
```

### Weekly Security Scans
```bash
# Run vulnerability scan
./vulnerability-scan.sh

# Review scan results
cat Z:/plane-data/security-scans/vulnerability_report_*.txt
```

### Monthly Data Export
```bash
# Create complete data export
./export-data.sh

# Verify export
ls -la Z:/plane-backups/exports/
```

## Recovery Procedures

### Database Recovery
```bash
# List available backups
ls -la Z:/plane-backups/postgres/

# Restore from backup
./restore-postgres.sh Z:/plane-backups/postgres/plane_backup_YYYYMMDD_HHMMSS.sql.gz
```

### Complete System Recovery
```bash
# 1. Restore database
./restore-postgres.sh <backup_file>

# 2. Restore uploads
cp -r Z:/plane-backups/exports/plane_export_*/uploads/* Z:/plane-data/uploads/

# 3. Restart services
docker-compose -f docker-compose.yml restart
```

## Multi-Agent Configuration

### API Token Management
1. Access Plane admin interface: http://localhost
2. Navigate to Settings > API Tokens
3. Create tokens for each LLM agent:
   - **Agent Type**: Service Token (300 req/min)
   - **Scope**: Project-specific or workspace-wide
   - **Expiration**: 90 days (recommended)

### Agent Access Control
```bash
# Monitor agent activity
docker-compose logs api | grep "API_TOKEN"

# Check rate limiting
docker-compose logs api | grep "rate_limit"
```

## Security Monitoring

### Log Monitoring
```bash
# Monitor API access
tail -f Z:/plane-data/logs/api/plane.log

# Monitor authentication attempts
docker-compose logs api | grep "authentication"
```

### Health Checks
```bash
# Check service health
docker-compose ps

# Verify database connectivity
docker exec plane-db pg_isready -U plane_admin

# Check disk usage
df -h Z:/plane-data/
```

## Troubleshooting

### Common Issues

**Issue**: Container fails to start with volume mount error
```bash
# Solution: Ensure NAS directories exist
./setup-nas-directories.sh
```

**Issue**: Database connection refused
```bash
# Solution: Check credentials in variables.env
docker-compose logs plane-db
```

**Issue**: High memory usage
```bash
# Solution: Adjust PostgreSQL settings
# Edit docker-compose.yml: postgres -c 'max_connections=25'
```

### Emergency Procedures
1. **Stop all services**: `docker-compose down`
2. **Backup current data**: `./backup-postgres.sh`
3. **Check logs**: `docker-compose logs`
4. **Restore from backup**: `./restore-postgres.sh <backup>`

## Security Best Practices

### Regular Maintenance
- [ ] Weekly vulnerability scans
- [ ] Monthly data exports
- [ ] Quarterly credential rotation
- [ ] Monitor disk space on NAS

### Access Control
- [ ] Limit API token scope to minimum required
- [ ] Set appropriate token expiration
- [ ] Monitor agent activity logs
- [ ] Implement agent timeout policies

### Data Protection
- [ ] Verify RAID 5 status on NAS
- [ ] Test backup restoration monthly
- [ ] Monitor backup storage usage
- [ ] Validate data export integrity

## Support and Documentation
- **Configuration**: `variables.env`
- **Logs**: `Z:/plane-data/logs/`
- **Backups**: `Z:/plane-backups/`
- **Exports**: `Z:/plane-backups/exports/`

For additional security considerations, see the complete security assessment in `docs/local_deployment_security_assessment.md`. 