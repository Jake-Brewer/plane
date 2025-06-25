# Plane MCP Server Setup Guide
# Last Updated: 2025-01-27

## Overview

The Plane MCP (Model Context Protocol) server enables native Cursor integration with your Plane project management platform. This guide will walk you through setting up authentication and configuring the integration.

## Prerequisites

1. **Plane Instance Running**: Ensure your Plane Docker containers are running
2. **Python Environment**: Python 3.8+ with required packages
3. **Cursor Editor**: Latest version with MCP support

## Step 1: Verify Plane is Running

Check that your Plane containers are active:

```powershell
docker ps
```

You should see containers including:
- `plane-working-proxy-1` (exposed on port 51534)
- `plane-working-api-1` 
- `plane-working-web-1`

## Step 2: Access Plane Web Interface

1. Open your browser to: `http://localhost:51534`
2. Complete the Plane setup if this is your first time
3. Create or log into your account

## Step 3: Create API Token

### Via Web Interface:
1. Go to **Settings** → **API Tokens**
2. Click **"Create API Token"**
3. Set a label (e.g., "MCP Server Integration")
4. Set expiration (optional, recommended: 90 days)
5. Click **Create**
6. **IMPORTANT**: Copy the token immediately - it won't be shown again

### Via API (Alternative):
```powershell
# Get workspace slug first
$workspaceResponse = Invoke-WebRequest -Uri "http://localhost:51534/api/workspaces/" -Headers @{"X-Api-Key"="your_existing_token"}

# Create new token
$body = @{
    label = "MCP Server Integration"
    description = "Token for Cursor MCP integration"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:51534/api/workspaces/YOUR_WORKSPACE_SLUG/api-tokens/" -Method POST -Body $body -Headers @{"Content-Type"="application/json"; "X-Api-Key"="your_existing_token"}
```

## Step 4: Configure Environment Variables

Create or update your environment variables:

### Option A: PowerShell Session (Temporary)
```powershell
$env:PLANE_API_URL = "http://localhost:51534"
$env:PLANE_API_KEY = "plane_api_your_token_here"
$env:PLANE_MCP_PORT = "43533"
```

### Option B: System Environment Variables (Permanent)
1. Open **System Properties** → **Environment Variables**
2. Add these variables:
   - `PLANE_API_URL` = `http://localhost:51534`
   - `PLANE_API_KEY` = `plane_api_your_token_here`
   - `PLANE_MCP_PORT` = `43533`

### Option C: .env File (Development)
Create `plane-mcp.env` file:
```env
PLANE_API_URL=http://localhost:51534
PLANE_API_KEY=plane_api_your_token_here
PLANE_MCP_PORT=43533
```

Load with: `Get-Content plane-mcp.env | ForEach-Object { $env:($_.Split('=')[0]) = $_.Split('=')[1] }`

## Step 5: Install Python Dependencies

```powershell
pip install fastapi httpx prometheus_client starlette uvicorn
```

## Step 6: Start the MCP Server

```powershell
python for_llm/plane-mcp-server.py
```

You should see:
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:43533 (Press CTRL+C to quit)
```

## Step 7: Test the Integration

Run the test script:
```powershell
.\test-mcp.ps1
```

Expected output:
```
✅ Metrics endpoint working - Status: 200
✅ Tools list endpoint working - Status: 200
✅ Plane API proxy working - Status: 200
```

## Step 8: Configure Cursor MCP Integration

### Manual Configuration:
1. Open Cursor Settings
2. Go to **Extensions** → **MCP Servers**
3. Add new server:
   - **Name**: `plane-mcp`
   - **URL**: `http://localhost:43533`
   - **Type**: `HTTP`

### Via MCP Config File:
Add to your Cursor MCP configuration:
```json
{
  "mcpServers": {
    "plane-mcp": {
      "command": "python",
      "args": ["for_llm/plane-mcp-server.py"],
      "env": {
        "PLANE_API_URL": "http://localhost:51534",
        "PLANE_API_KEY": "plane_api_your_token_here",
        "PLANE_MCP_PORT": "43533"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues:

#### 1. "Authentication credentials were not provided"
- **Cause**: Missing or invalid API key
- **Solution**: Verify your `PLANE_API_KEY` environment variable
- **Test**: `echo $env:PLANE_API_KEY` (should show your token)

#### 2. "Connection refused" on port 43533
- **Cause**: MCP server not running
- **Solution**: Start the server with `python for_llm/plane-mcp-server.py`

#### 3. "Connection refused" on port 51534
- **Cause**: Plane containers not running
- **Solution**: Start Plane with `docker-compose up -d`

#### 4. "Internal Server Error" from API proxy
- **Cause**: Incorrect API endpoint or authentication
- **Solution**: Check Plane logs with `docker logs plane-working-api-1`

### Verification Commands:

```powershell
# Check environment variables
Get-ChildItem Env: | Where-Object {$_.Name -like "*PLANE*"}

# Test direct API access
$headers = @{"X-Api-Key"="$env:PLANE_API_KEY"}
Invoke-WebRequest -Uri "$env:PLANE_API_URL/api/workspaces/" -Headers $headers -UseBasicParsing

# Check MCP server health
Invoke-WebRequest -Uri "http://localhost:43533/metrics" -UseBasicParsing

# Test MCP tools endpoint
$body = '{}'; $headers = @{'Content-Type'='application/json'}
Invoke-WebRequest -Uri "http://localhost:43533/tools/list" -Method POST -Body $body -Headers $headers -UseBasicParsing
```

## Available MCP Tools

Once configured, you'll have access to these Plane operations through Cursor:

### Workspace Management
- List workspaces
- Get workspace details

### Project Management  
- List projects in workspace
- Get project details
- Create new projects

### Issue Management
- List issues with filtering
- Get issue details
- Create new issues
- Update existing issues

### Team & Organization
- List workspace/project members
- Get project analytics
- Manage labels and states

### Cycle Management
- List project cycles
- Create new cycles

## Security Considerations

1. **API Key Security**: Never commit API keys to version control
2. **Network Security**: MCP server runs on localhost only by default
3. **Token Expiration**: Set reasonable expiration dates for API tokens
4. **Access Control**: Use workspace-specific tokens when possible

## Monitoring & Metrics

The MCP server exposes Prometheus metrics at `http://localhost:43533/metrics`:

- `plane_mcp_requests_total`: Total requests by endpoint/method/status
- `plane_mcp_request_latency_seconds`: Request latency by endpoint/method

## Next Steps

1. **Test Integration**: Create a test issue through Cursor
2. **Workflow Setup**: Configure your preferred Plane workflows
3. **Team Onboarding**: Share setup guide with team members
4. **Automation**: Explore advanced MCP automation possibilities

## Support

- **GitHub Issues**: Report bugs in the Plane repository
- **Discord**: Join the Plane community for real-time help
- **Documentation**: Visit docs.plane.so for detailed API documentation

---

**Last Updated**: 2025-01-27  
**Version**: 1.0.0  
**Compatibility**: Plane v0.21+, Cursor v0.42+ 