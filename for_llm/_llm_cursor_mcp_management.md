# Cursor MCP Server Management Guide
# Last Updated: 2025-01-27T00:00:00Z

## Overview

This guide provides comprehensive instructions for managing Model Context Protocol (MCP) servers in Cursor, including installation, configuration, backup, and troubleshooting procedures.

## MCP Server Basics

### What is MCP?
Model Context Protocol (MCP) enables AI assistants to connect to external systems and services through standardized interfaces. In Cursor, MCP servers provide tools that LLMs can use to interact with APIs, databases, and other resources.

### MCP Configuration Location
**Windows**: `C:\Users\USERNAME\AppData\Roaming\Cursor\User\mcp.json`
**macOS**: `~/Library/Application Support/Cursor/User/mcp.json`
**Linux**: `~/.config/Cursor/User/mcp.json`

## Installation & Configuration

### Adding a New MCP Server

#### 1. Prepare Server Configuration
Create your MCP server configuration in `for_llm/cursor-mcp-config.json`:

```json
{
  "mcpServers": {
    "plane": {
      "command": "node",
      "args": ["D:\\repos\\cursor-projects\\categories\\organization\\project-management\\plane-working\\for_llm\\plane-mcp-server.js"],
      "env": {
        "PLANE_API_URL": "http://localhost:51534",
        "PLANE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### 2. Backup Existing Configuration
**Always backup before making changes!**

```powershell
# Windows PowerShell
$mcpPath = "$env:APPDATA\Cursor\User\mcp.json"
$backupPath = ".\backups\mcp-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
Copy-Item $mcpPath $backupPath
```

#### 3. Install MCP Server
```powershell
# Copy configuration to Cursor
$sourcePath = ".\for_llm\cursor-mcp-config.json"
$targetPath = "$env:APPDATA\Cursor\User\mcp.json"
Copy-Item $sourcePath $targetPath
```

#### 4. Restart Cursor
Close and restart Cursor completely for MCP changes to take effect.

### MCP Server Types

#### Node.js Servers
```json
{
  "command": "node",
  "args": ["path/to/server.js"],
  "env": {
    "API_KEY": "value"
  }
}
```

#### Python Servers
```json
{
  "command": "python",
  "args": ["path/to/server.py"],
  "env": {
    "PYTHONPATH": "path/to/modules"
  }
}
```

#### Executable Servers
```json
{
  "command": "path/to/executable",
  "args": ["--config", "config.json"],
  "env": {}
}
```

## Backup & Recovery Procedures

### Automated Backup System

#### Create Backup Directory Structure
```powershell
# Create backup directory
New-Item -ItemType Directory -Path ".\backups\mcp-configs" -Force

# Create backup script
@"
# MCP Configuration Backup Script
`$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
`$mcpPath = "`$env:APPDATA\Cursor\User\mcp.json"
`$backupPath = ".\backups\mcp-configs\mcp-backup-`$timestamp.json"

if (Test-Path `$mcpPath) {
    Copy-Item `$mcpPath `$backupPath
    Write-Host "MCP configuration backed up to: `$backupPath"
} else {
    Write-Host "No MCP configuration found at: `$mcpPath"
}
"@ | Out-File -FilePath ".\scripts\backup-mcp.ps1" -Encoding UTF8
```

#### Restore from Backup
```powershell
# List available backups
Get-ChildItem ".\backups\mcp-configs\*.json" | Sort-Object LastWriteTime -Descending

# Restore specific backup
$backupFile = ".\backups\mcp-configs\mcp-backup-TIMESTAMP.json"
$mcpPath = "$env:APPDATA\Cursor\User\mcp.json"
Copy-Item $backupFile $mcpPath
```

### Version Control Integration
```powershell
# Add MCP configurations to git
git add backups/mcp-configs/
git add for_llm/cursor-mcp-config.json
git commit -m "Backup MCP configuration before changes"
```

## MCP Server Development

### Creating Custom MCP Servers

#### Basic Server Structure (Node.js)
```javascript
#!/usr/bin/env node

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

class CustomMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'custom-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );
    
    this.setupTools();
  }

  setupTools() {
    // Define your tools here
    this.server.setRequestHandler('tools/list', async () => {
      return {
        tools: [
          {
            name: 'example_tool',
            description: 'An example tool',
            inputSchema: {
              type: 'object',
              properties: {
                input: { type: 'string' }
              }
            }
          }
        ]
      };
    });

    this.server.setRequestHandler('tools/call', async (request) => {
      // Handle tool calls
      return {
        content: [
          {
            type: 'text',
            text: 'Tool executed successfully'
          }
        ]
      };
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}

// Start server
const server = new CustomMCPServer();
server.run().catch(console.error);
```

#### Testing MCP Servers
```powershell
# Test server directly
node path/to/mcp-server.js

# Test with MCP client
npx @modelcontextprotocol/inspector path/to/mcp-server.js
```

## Troubleshooting

### Common Issues

#### 1. MCP Server Not Loading
**Symptoms**: Tools not available in Cursor
**Solutions**:
- Check server path is correct and file exists
- Verify Node.js/Python is installed and in PATH
- Check server logs for errors
- Restart Cursor completely

#### 2. Environment Variables Not Working
**Symptoms**: Server starts but API calls fail
**Solutions**:
- Verify environment variables in mcp.json
- Check API keys and URLs are correct
- Test API connectivity outside of MCP

#### 3. Permission Errors
**Symptoms**: Server fails to start with permission errors
**Solutions**:
- Check file permissions on server script
- Run Cursor as administrator (Windows)
- Verify script is executable (Unix)

### Diagnostic Commands

#### Check MCP Configuration
```powershell
# View current MCP configuration
Get-Content "$env:APPDATA\Cursor\User\mcp.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

#### Test Server Connectivity
```powershell
# Test if server script exists and is executable
Test-Path "path/to/server.js"

# Test Node.js availability
node --version

# Test server startup (manual)
node "path/to/server.js"
```

#### Debug Server Issues
```javascript
// Add logging to your MCP server
console.error('MCP Server starting...');
console.error('Environment variables:', process.env);
console.error('Arguments:', process.argv);
```

## Security Best Practices

### API Key Management
1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Rotate keys regularly** and update configurations
4. **Limit API key permissions** to minimum required

### Server Security
1. **Validate all inputs** in MCP tools
2. **Sanitize outputs** before returning to LLM
3. **Implement rate limiting** for API calls
4. **Log security events** for monitoring

### Configuration Security
1. **Backup configurations** before changes
2. **Use secure file permissions** on config files
3. **Audit MCP server access** regularly
4. **Monitor for unauthorized changes**

## Advanced Configuration

### Multiple Server Management
```json
{
  "mcpServers": {
    "plane": {
      "command": "node",
      "args": ["./servers/plane-mcp-server.js"],
      "env": { "PLANE_API_URL": "http://localhost:51534" }
    },
    "github": {
      "command": "node", 
      "args": ["./servers/github-mcp-server.js"],
      "env": { "GITHUB_TOKEN": "ghp_xxxx" }
    },
    "database": {
      "command": "python",
      "args": ["./servers/db-server.py"],
      "env": { "DB_CONNECTION": "postgresql://..." }
    }
  }
}
```

### Conditional Server Loading
```json
{
  "mcpServers": {
    "development-only": {
      "command": "node",
      "args": ["./dev-server.js"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  }
}
```

## Maintenance Procedures

### Regular Maintenance Tasks
1. **Weekly**: Check server logs for errors
2. **Monthly**: Update MCP server dependencies
3. **Quarterly**: Review and update API keys
4. **Annually**: Audit server permissions and access

### Update Procedures
1. **Backup current configuration**
2. **Test updates in development**
3. **Deploy during low-usage periods**
4. **Monitor for issues after deployment**
5. **Rollback if problems occur**

---

## Quick Reference

### Add New MCP Server
1. Create server configuration in `for_llm/cursor-mcp-config.json`
2. Backup existing MCP configuration
3. Copy configuration to Cursor directory
4. Restart Cursor
5. Test server functionality

### Backup MCP Configuration
```powershell
Copy-Item "$env:APPDATA\Cursor\User\mcp.json" ".\backups\mcp-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
```

### Restore MCP Configuration
```powershell
Copy-Item ".\backups\mcp-backup-TIMESTAMP.json" "$env:APPDATA\Cursor\User\mcp.json"
```

**Remember**: Always backup MCP configurations before making changes, and test thoroughly in development environments before deploying to production. 