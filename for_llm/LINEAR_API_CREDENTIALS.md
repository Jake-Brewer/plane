# Linear API Credentials & Authentication
# Last Updated: 2025-01-27T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## Overview

This guide provides comprehensive instructions for setting up and managing Linear API authentication, including OAuth setup, API key management, and troubleshooting connection issues. Linear integration is essential for project management and issue tracking.

---

## Authentication Methods

### OAuth Authentication (Recommended)
- **Security**: Most secure method with token refresh capabilities
- **User Experience**: Seamless user experience with login flow
- **Permissions**: Granular permission control
- **Token Management**: Automatic token refresh
- **Audit Trail**: Complete audit trail of API access

### API Key Authentication
- **Simplicity**: Simple setup and configuration
- **Reliability**: Most reliable for automated systems
- **Performance**: Fast authentication with minimal overhead
- **Control**: Direct control over API access
- **Limitations**: Manual token management required

### Connection Methods Available
The global MCP configuration supports 5 different connection methods:
1. **linear-oauth**: OAuth SSE server (may require login)
2. **linear**: mcp-remote method
3. **linear-advanced**: Third-party server (@cosmix/linear-mcp-server)
4. **linear-api**: Direct API key (most reliable)
5. **linear-local**: Local server backup

---

## OAuth Setup

### Initial Configuration
1. **Linear Application Registration**
   - Go to Linear Settings → API → OAuth Applications
   - Create new OAuth application
   - Set redirect URI to match your configuration
   - Note the Client ID and Client Secret

2. **Environment Configuration**
   ```bash
   LINEAR_CLIENT_ID=your_client_id_here
   LINEAR_CLIENT_SECRET=your_client_secret_here
   LINEAR_REDIRECT_URI=http://localhost:3000/auth/callback
   ```

3. **MCP Server Configuration**
   ```json
   {
     "linear-oauth": {
       "command": "node",
       "args": ["linear-oauth-server.js"],
       "env": {
         "LINEAR_CLIENT_ID": "your_client_id",
         "LINEAR_CLIENT_SECRET": "your_client_secret"
       }
     }
   }
   ```

### OAuth Flow
1. **Authorization Request**: User is redirected to Linear authorization page
2. **User Consent**: User grants permissions to the application
3. **Authorization Code**: Linear returns authorization code
4. **Token Exchange**: Exchange authorization code for access token
5. **Token Storage**: Store access token securely
6. **Token Refresh**: Automatically refresh tokens when expired

---

## API Key Setup

### Obtaining API Key
1. **Linear Settings**: Go to Linear Settings → API
2. **Create API Key**: Click "Create API Key"
3. **Set Permissions**: Configure appropriate permissions
4. **Copy Key**: Copy the generated API key (shown only once)
5. **Secure Storage**: Store the API key securely

### API Key Configuration
```bash
# Environment variable
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxx

# MCP Configuration
{
  "linear-api": {
    "command": "node",
    "args": ["linear-api-server.js"],
    "env": {
      "LINEAR_API_KEY": "lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### API Key Best Practices
- **Secure Storage**: Never store API keys in code or version control
- **Environment Variables**: Use environment variables for API keys
- **Rotation**: Regularly rotate API keys
- **Minimal Permissions**: Grant only necessary permissions
- **Monitoring**: Monitor API key usage for unusual activity

---

## Global MCP Configuration

### Configuration File Location
The Linear MCP is globally configured in:
```
C:\Users\jake_\.cursor\mcp.json
```

### Complete Configuration Example
```json
{
  "mcpServers": {
    "linear-oauth": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_CLIENT_ID": "your_client_id",
        "LINEAR_CLIENT_SECRET": "your_client_secret"
      }
    },
    "linear": {
      "command": "mcp-remote",
      "args": ["linear-server"],
      "env": {
        "LINEAR_API_KEY": "your_api_key"
      }
    },
    "linear-advanced": {
      "command": "npx",
      "args": ["-y", "@cosmix/linear-mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your_api_key"
      }
    },
    "linear-api": {
      "command": "node",
      "args": ["linear-direct-api.js"],
      "env": {
        "LINEAR_API_KEY": "your_api_key"
      }
    },
    "linear-local": {
      "command": "node",
      "args": ["local-linear-server.js"],
      "env": {
        "LINEAR_API_KEY": "your_api_key"
      }
    }
  }
}
```

---

## Connection Validation

### Testing OAuth Connection
```javascript
// Test OAuth token
async function testOAuthConnection() {
  const token = await getOAuthToken();
  const response = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: 'query { viewer { id name email } }'
    })
  });
  
  const data = await response.json();
  console.log('OAuth Connection Test:', data);
}
```

### Testing API Key Connection
```javascript
// Test API key
async function testApiKeyConnection() {
  const response = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: {
      'Authorization': process.env.LINEAR_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: 'query { viewer { id name email } }'
    })
  });
  
  const data = await response.json();
  console.log('API Key Connection Test:', data);
}
```

### Connection Health Check
```bash
# Test MCP server connection
curl -X POST http://localhost:3000/health \
  -H "Content-Type: application/json" \
  -d '{"method": "ping"}'
```

---

## Troubleshooting

### Common Issues

#### OAuth Issues
- **Invalid Client ID**: Verify client ID matches Linear application
- **Invalid Redirect URI**: Ensure redirect URI matches configuration
- **Token Expired**: Implement automatic token refresh
- **Scope Issues**: Verify requested scopes are authorized
- **Network Issues**: Check network connectivity and firewall settings

#### API Key Issues
- **Invalid API Key**: Verify API key is correct and active
- **Insufficient Permissions**: Check API key permissions
- **Rate Limiting**: Implement rate limiting and retry logic
- **Network Issues**: Check connectivity to Linear API
- **Key Expiration**: Check if API key has expired

#### MCP Server Issues
- **Server Not Running**: Verify MCP server is running
- **Port Conflicts**: Check for port conflicts
- **Configuration Errors**: Validate MCP configuration
- **Environment Variables**: Verify environment variables are set
- **Dependencies**: Check all dependencies are installed

### Diagnostic Commands
```bash
# Check MCP server status
ps aux | grep linear

# Check environment variables
echo $LINEAR_API_KEY
echo $LINEAR_CLIENT_ID

# Test API connectivity
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { viewer { id } }"}'

# Check MCP configuration
cat ~/.cursor/mcp.json | jq '.mcpServers["linear-api"]'
```

### Error Resolution
- **Authentication Errors**: Re-authenticate with Linear
- **Permission Errors**: Update API key or OAuth permissions  
- **Network Errors**: Check network connectivity and firewall
- **Configuration Errors**: Validate and update configuration
- **Server Errors**: Restart MCP servers and check logs

---

## Security Best Practices

### Credential Management
- **Environment Variables**: Store credentials in environment variables
- **Secure Storage**: Use secure credential storage systems
- **Access Control**: Limit access to credentials
- **Rotation**: Regularly rotate credentials
- **Monitoring**: Monitor credential usage

### Network Security
- **HTTPS Only**: Use HTTPS for all API communications
- **Certificate Validation**: Validate SSL certificates
- **Network Isolation**: Isolate API communications
- **Firewall Rules**: Configure appropriate firewall rules
- **VPN Access**: Use VPN for sensitive operations

### Audit and Monitoring
- **Access Logging**: Log all API access
- **Error Monitoring**: Monitor and alert on errors
- **Usage Tracking**: Track API usage patterns
- **Security Events**: Monitor for security events
- **Regular Audits**: Conduct regular security audits

---

## Maintenance Procedures

### Regular Maintenance
- **Token Refresh**: Ensure automatic token refresh works
- **Connection Testing**: Regularly test all connections
- **Log Review**: Review logs for errors or issues
- **Performance Monitoring**: Monitor API performance
- **Security Updates**: Apply security updates promptly

### Emergency Procedures
- **Token Revocation**: Revoke compromised tokens immediately
- **Fallback Systems**: Activate fallback authentication systems
- **Incident Response**: Follow incident response procedures
- **Communication**: Communicate issues to stakeholders
- **Recovery**: Implement recovery procedures

### Documentation Updates
- **Configuration Changes**: Document all configuration changes
- **Procedure Updates**: Update procedures based on experience
- **Troubleshooting Guides**: Update troubleshooting information
- **Security Policies**: Update security policies as needed
- **Training Materials**: Update training materials regularly 