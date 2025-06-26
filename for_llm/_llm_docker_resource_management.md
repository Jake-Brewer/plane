# Docker Resource Management Strategy

# Last Updated: 2025-06-25T10:30:00Z

This document outlines our strategy for managing Docker resources to avoid conflicts and ensure proper isolation between different branches and deployments.

## Container Naming Convention

- **Pattern**: `{prefix}-{service}`
- **Enhanced Security Monitoring**: `esm-` prefix (e.g., `esm-api`, `esm-web`)
- **Shared Infrastructure**: `shared-` prefix (e.g., `shared-postgres`, `shared-redis`)
- **Branch-specific Deployments**: `plane-{branch}-{service}` (e.g., `plane-develop-web`, `plane-feature-enhanced-security-web`)

## Branch Management Approach

- Structured deployment allowing multiple branches to run simultaneously
- Branch-specific folders (e.g., `plane-develop/`, `plane-feature-enhanced-security-monitoring/`) each contain their own docker-compose.yml
- Each branch deployment has unique container names and port mappings to avoid conflicts

## Port Allocation Rules

- **Master branch**: Web UI on port 8080, API on port 9000
- **Develop branch**: Web UI on port 8081, API on port 9001
- **Feature branches**: Web UI starting at 8082+, API starting at 9002+

## Environment Variables

- Security-focused deployment with appropriate defaults
- All external telemetry redirected to local storage with "DISABLED_REDIRECT_TO_LOCAL" pattern
- Consistent credential patterns for database, S3, and message queue services

## Network Organization

- Shared network named `shared-network` for common resources
- Branch-specific networks named `plane-{branch}-network` for isolation

## Auto-detection for MCP Server

When developing MCP servers that need to connect to Plane API:

- First check for direct environment variable configuration (PLANE_API_URL)
- If not found, attempt to auto-detect based on Docker container naming patterns
- Default to port mapping rules above based on detected branch name
- Store port information in cache for subsequent requests
