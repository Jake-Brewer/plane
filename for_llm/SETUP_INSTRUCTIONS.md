# Plane-Cursor Integration Setup Instructions
# Last Updated: 2025-01-27T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## 🚀 **Quick Setup Guide**

This guide will set up the optimal Plane-Cursor integration using the MCP server approach for native Cursor integration.

---

## **Prerequisites**

### **1. Plane Installation**
Ensure Plane is running locally:
```bash
# Check if Plane is running
curl http://localhost:8000/api/health/

# If not running, start Plane development environment
cd plane-working
docker-compose up -d  # or your preferred method
```

### **2. Node.js Environment**
- **Node.js 18+** installed
- **npm** or **yarn** package manager

### **3. Cursor with MCP Support**
- **Cursor IDE** with MCP server support
- Access to `~/.cursor/mcp.json` configuration

---

## **Step 1: Install Dependencies**

```bash
cd for_llm
npm install
```

## **Step 2: Configure API Access**

### **2.1 Get Plane API Key**
1. Open Plane in your browser: `http://localhost:8000`
2. Navigate to **Settings** → **API** → **Create API Token**
3. Copy the generated API key

### **2.2 Set Environment Variables**
Copy the environment template and configure:
```bash
# Copy the template
cp plane-env-template.txt .env

# Edit with your values
nano .env  # or your preferred editor
```

Required environment variables:
```bash
PLANE_API_URL=http://localhost:8000
PLANE_API_KEY=your_actual_api_key_here
PLANE_DEFAULT_WORKSPACE=your-workspace-slug
PLANE_DEFAULT_PROJECT=your-project-id
```

## **Step 3: Test Integration**

Run the integration test to validate setup:
```bash
cd for_llm
npm test
```

Expected output:
```
🚀 Starting Plane Integration Tests
✅ Successfully connected to Plane API
✅ Found workspace: My Workspace (my-workspace)
✅ Found project: Sample Project (abc123)
✅ All tests passed! Plane integration is ready.
```

## **Step 4: Configure Cursor MCP**

### **4.1 Locate Cursor Configuration**
Find your Cursor MCP configuration file:
- **Windows**: `%APPDATA%\Cursor\User\mcp.json`
- **macOS**: `~/Library/Application Support/Cursor/User/mcp.json`
- **Linux**: `~/.config/Cursor/User/mcp.json`

### **4.2 Add Plane MCP Server**
Edit the `mcp.json` file and add the Plane server configuration:

```json
{
  "mcpServers": {
    "plane": {
      "command": "node",
      "args": ["D:/repos/cursor-projects/categories/organization/project-management/plane-working/for_llm/plane-mcp-server.js"],
      "env": {
        "PLANE_API_URL": "http://localhost:8000",
        "PLANE_API_KEY": "your_actual_api_key_here",
        "PLANE_DEFAULT_WORKSPACE": "your-workspace-slug",
        "PLANE_DEFAULT_PROJECT": "your-project-id"
      }
    }
  }
}
```

**Note**: Update the file path to match your actual installation directory.

### **4.3 Restart Cursor**
1. Close Cursor completely
2. Restart Cursor
3. The MCP server will be automatically loaded

## **Step 5: Verify Cursor Integration**

### **5.1 Test MCP Server**
In a new Cursor conversation, try:
```
List all workspaces in Plane
```

### **5.2 Test Issue Management**
```
Create a new issue in the default project called "Test LLM Integration"
```

### **5.3 Test Project Operations**
```
Show me all projects in the workspace
```

---

## **Available Commands**

Once configured, you can use these commands in Cursor conversations:

### **Workspace Management**
- `List all workspaces`
- `Get workspace details for [workspace-slug]`

### **Project Management**
- `List all projects in [workspace-slug]`
- `Create a new project called [name] in [workspace-slug]`
- `Get project details for [project-id]`

### **Issue Management**
- `List issues in [project-id]`
- `Create issue "[title]" with description "[description]"`
- `Update issue [issue-id] to set priority to high`
- `Get issue details for [issue-id]`

### **Team Management**
- `List all members in [workspace-slug]`
- `List project members for [project-id]`

### **Analytics**
- `Get project analytics for [project-id]`
- `Show project statistics`

---

## **Advanced Configuration**

### **Production Setup**
For production Plane instances, update the environment:
```bash
PLANE_API_URL=https://your-plane-instance.com
PLANE_API_KEY=your_production_api_key
```

### **Multiple Environments**
You can configure multiple MCP servers for different environments:
```json
{
  "mcpServers": {
    "plane-local": {
      "command": "node",
      "args": ["path/to/plane-mcp-server.js"],
      "env": {
        "PLANE_API_URL": "http://localhost:8000",
        "PLANE_API_KEY": "local_api_key"
      }
    },
    "plane-staging": {
      "command": "node", 
      "args": ["path/to/plane-mcp-server.js"],
      "env": {
        "PLANE_API_URL": "https://staging.plane.com",
        "PLANE_API_KEY": "staging_api_key"
      }
    }
  }
}
```

### **Custom Resource Access**
Access Plane resources directly:
```
Get resource plane://workspace/my-workspace
Get resource plane://project/my-workspace/project-123
Get resource plane://issue/my-workspace/project-123/issue-456
```

---

## **Troubleshooting**

### **Connection Issues**
1. **Verify Plane is running**: `curl http://localhost:8000/api/health/`
2. **Check API key**: Ensure it's valid and has proper permissions
3. **Test manually**: Run `npm test` in the `for_llm` directory

### **MCP Server Issues**
1. **Check Cursor logs**: Look for MCP-related errors in Cursor console
2. **Verify file paths**: Ensure the MCP configuration uses correct absolute paths
3. **Test server directly**: Run `node plane-mcp-server.js` manually

### **Permission Issues**
1. **API key permissions**: Ensure the API key has workspace access
2. **Project access**: Verify you have access to the specified projects
3. **Network access**: Check firewall settings for local connections

### **Common Error Messages**

**"Failed to connect to Plane API"**
- Check if Plane is running on the specified URL
- Verify API key is correct
- Check network connectivity

**"Workspace not found"**
- Verify workspace slug is correct
- Check API key has access to the workspace

**"MCP server not responding"**
- Restart Cursor completely
- Check MCP configuration file syntax
- Verify file paths in configuration

---

## **Next Steps**

Once setup is complete, you can:

1. **Create Linear Integration**: Set up bidirectional sync with Linear
2. **Add Custom Commands**: Extend the MCP server with project-specific tools
3. **Integrate with CI/CD**: Connect issue management to deployment workflows
4. **Add Analytics**: Create custom reporting and analytics tools

---

## **Support and Resources**

- **Plane Documentation**: https://docs.plane.so
- **MCP Documentation**: https://spec.modelcontextprotocol.io
- **API Reference**: http://localhost:8000/api/docs/ (when running locally)
- **Project Issues**: Use GitHub issues for bug reports and feature requests

---

**Remember**: This integration provides native Cursor access to all Plane functionality while maintaining the existing Django REST API architecture. The MCP server acts as a bridge, providing type-safe, documented access to Plane's project management capabilities. 