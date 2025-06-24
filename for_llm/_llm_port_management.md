# Port Management & Configuration Guide
# Last Updated: 2025-01-27T00:00:00Z

## Overview

This guide provides comprehensive instructions for managing ports in development environments, including conflict detection, random port generation, and configuration updates across all project files.

## Port Selection Strategy

### Random Port Generation
1. **Use Random.org** for true randomness when possible
2. **Fallback to system random** for automated processes
3. **Port Range**: Use 10000-65535 (avoid well-known ports 0-1023 and registered ports 1024-49151)
4. **Conflict Detection**: Always check for existing usage before assignment

### Port Conflict Detection

#### Windows (PowerShell)
```powershell
# Check if specific port is in use
netstat -ano | findstr ":PORT_NUMBER"

# Check range of ports
netstat -ano | findstr ":1[0-9][0-9][0-9][0-9]"

# Generate random port and check availability
$port = Get-Random -Minimum 10000 -Maximum 65535
$inUse = netstat -ano | findstr ":$port"
if (-not $inUse) { Write-Host "Port $port is available" }
```

#### Linux/Mac
```bash
# Check if specific port is in use
netstat -tuln | grep :PORT_NUMBER
lsof -i :PORT_NUMBER

# Check if port is available
if ! netstat -tuln | grep -q :PORT_NUMBER; then
    echo "Port PORT_NUMBER is available"
fi
```

## Configuration Update Procedures

### Files to Update for Port Changes

#### Docker Configuration
- `docker-compose.yml` - Main production configuration
- `docker-compose-local.yml` - Local development configuration

#### Cursor Integration
- `for_llm/plane-local.env` - Environment variables
- `for_llm/cursor-mcp-config.json` - MCP server configuration
- `for_llm/setup-cursor-integration.ps1` - Setup script

#### Documentation
- `for_llm/PLANE_PORT_UPDATE_STATUS.md` - Status tracking
- Any port-specific documentation files

### Automated Port Update Script

```powershell
# PowerShell script for updating all port configurations
param(
    [Parameter(Mandatory=$true)]
    [int]$NewPort,
    [int]$OldPort = 8080
)

# Validate port availability
$inUse = netstat -ano | findstr ":$NewPort"
if ($inUse) {
    Write-Error "Port $NewPort is already in use!"
    exit 1
}

# Files to update
$filesToUpdate = @(
    "docker-compose.yml",
    "docker-compose-local.yml", 
    "for_llm/plane-local.env",
    "for_llm/cursor-mcp-config.json",
    "for_llm/setup-cursor-integration.ps1"
)

# Update each file
foreach ($file in $filesToUpdate) {
    if (Test-Path $file) {
        Write-Host "Updating $file..."
        (Get-Content $file) -replace ":$OldPort", ":$NewPort" | Set-Content $file
        (Get-Content $file) -replace "localhost:$OldPort", "localhost:$NewPort" | Set-Content $file
    }
}

Write-Host "Port updated from $OldPort to $NewPort in all configuration files"
```

## Port Management Best Practices

### Development Environment
1. **Use high-numbered ports** (10000+) to avoid conflicts
2. **Document port assignments** in project documentation
3. **Test port availability** before assignment
4. **Update all related configurations** atomically
5. **Commit changes together** with descriptive messages

### Production Environment
1. **Use standard ports** where appropriate (80, 443, 8080)
2. **Configure load balancers** and proxies accordingly
3. **Update firewall rules** if necessary
4. **Coordinate with infrastructure team** for port assignments

### Docker Considerations
1. **External vs Internal ports** - Map external random ports to standard internal ports
2. **Port conflicts** - Check host system before container startup
3. **Service discovery** - Update service configurations when ports change
4. **Health checks** - Verify services are accessible on new ports

## Troubleshooting

### Common Issues
1. **Port already in use** - Check for other services, restart if necessary
2. **Firewall blocking** - Verify firewall rules allow traffic
3. **Service not binding** - Check service configuration and logs
4. **Proxy misconfiguration** - Verify reverse proxy settings

### Diagnostic Commands
```powershell
# Windows diagnostics
netstat -ano | findstr ":PORT"           # Check port usage
Test-NetConnection localhost -Port PORT   # Test connectivity
Get-Process -Id PID                       # Identify process using port

# Service-specific checks
docker ps --format "table {{.Names}}\t{{.Ports}}"  # Docker port mappings
docker logs CONTAINER_NAME                          # Container logs
```

## Integration with Other Systems

### Cursor MCP Configuration
When updating ports, ensure MCP server configuration is updated:
1. Update `cursor-mcp-config.json`
2. Backup existing configuration
3. Restart Cursor after changes
4. Test MCP server connectivity

### CI/CD Considerations
1. **Environment variables** - Update deployment configurations
2. **Health checks** - Modify readiness/liveness probes
3. **Service mesh** - Update service discovery configurations
4. **Monitoring** - Update monitoring and alerting rules

## Security Considerations

### Port Security
1. **Minimize exposed ports** - Only expose necessary services
2. **Use non-standard ports** for security through obscurity
3. **Implement proper authentication** regardless of port
4. **Monitor port usage** for unauthorized services

### Network Security
1. **Firewall configuration** - Restrict access to development ports
2. **VPN requirements** - Use VPN for accessing development services
3. **SSL/TLS** - Encrypt traffic even on non-standard ports
4. **Access logging** - Log access attempts for security monitoring

---

## Quick Reference

### Generate Random Port
```powershell
Get-Random -Minimum 10000 -Maximum 65535
```

### Check Port Availability
```powershell
netstat -ano | findstr ":PORT_NUMBER"
```

### Update Configuration Files
1. Update docker-compose files
2. Update MCP configuration
3. Update environment files
4. Update documentation
5. Test connectivity
6. Commit changes

**Remember**: Always test port changes in development before applying to production environments. 