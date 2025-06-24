# Plane-Cursor LLM Integration Guide
# Last Updated: 2025-01-27T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## Overview

This guide provides multiple approaches for LLMs to interact with Plane from Cursor conversations, leveraging the existing Django REST API, authentication systems, and integration patterns already established in the project.

---

## Integration Approaches

### 🎯 **Approach 1: Direct API Integration (Recommended)**

**Advantages:**
- Uses existing Django REST API endpoints
- Leverages established authentication patterns
- Full access to all Plane functionality
- Real-time data access
- Consistent with existing integration patterns

**Implementation:**
```typescript
// Create LLM-specific API service
class PlaneLLMService extends APIService {
  constructor() {
    super('http://localhost:8000'); // Local Plane instance
  }

  // Issue Management
  async createIssue(workspaceSlug: string, projectId: string, data: {
    name: string;
    description?: string;
    priority?: 'urgent' | 'high' | 'medium' | 'low' | 'none';
    assignees?: string[];
    labels?: string[];
    state?: string;
    parent?: string;
  }) {
    return this.post(`/api/workspaces/${workspaceSlug}/projects/${projectId}/issues/`, data);
  }

  // Project Management
  async getProjects(workspaceSlug: string) {
    return this.get(`/api/workspaces/${workspaceSlug}/projects/`);
  }

  // Workspace Management
  async getWorkspaces() {
    return this.get('/api/workspaces/');
  }

  // Analytics and Reporting
  async getProjectAnalytics(workspaceSlug: string, projectId: string) {
    return this.get(`/api/workspaces/${workspaceSlug}/projects/${projectId}/analytics/`);
  }
}
```

### 🔌 **Approach 2: MCP Server Integration**

**Advantages:**
- Native Cursor integration
- Follows established MCP patterns
- Automatic tool discovery
- Consistent with Linear integration approach

**Implementation:**
```javascript
// plane-mcp-server.js
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

class PlaneMCPServer {
  constructor() {
    this.server = new Server({
      name: 'plane-mcp-server',
      version: '1.0.0'
    });
    
    this.setupTools();
  }

  setupTools() {
    // Issue Management Tools
    this.server.tool('create_issue', {
      description: 'Create a new issue in Plane',
      parameters: {
        workspace_slug: { type: 'string', required: true },
        project_id: { type: 'string', required: true },
        name: { type: 'string', required: true },
        description: { type: 'string' },
        priority: { type: 'string', enum: ['urgent', 'high', 'medium', 'low', 'none'] }
      }
    }, this.createIssue.bind(this));

    this.server.tool('get_issues', {
      description: 'Get issues from a project',
      parameters: {
        workspace_slug: { type: 'string', required: true },
        project_id: { type: 'string', required: true },
        filters: { type: 'object' }
      }
    }, this.getIssues.bind(this));

    // Project Management Tools
    this.server.tool('get_projects', {
      description: 'Get all projects in a workspace',
      parameters: {
        workspace_slug: { type: 'string', required: true }
      }
    }, this.getProjects.bind(this));
  }

  async createIssue(params) {
    const response = await fetch(`${process.env.PLANE_API_URL}/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/issues/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.PLANE_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    });
    return response.json();
  }

  async getIssues(params) {
    const url = new URL(`${process.env.PLANE_API_URL}/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/issues/`);
    if (params.filters) {
      Object.entries(params.filters).forEach(([key, value]) => {
        url.searchParams.append(key, value);
      });
    }
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${process.env.PLANE_API_KEY}`
      }
    });
    return response.json();
  }

  async getProjects(params) {
    const response = await fetch(`${process.env.PLANE_API_URL}/api/workspaces/${params.workspace_slug}/projects/`, {
      headers: {
        'Authorization': `Bearer ${process.env.PLANE_API_KEY}`
      }
    });
    return response.json();
  }
}

// Start server
const server = new PlaneMCPServer();
const transport = new StdioServerTransport();
server.connect(transport);
```

### 🌐 **Approach 3: Web Interface Automation**

**Advantages:**
- No API key required
- Uses existing web interface
- Can leverage all UI features
- Good for complex workflows

**Implementation:**
```typescript
// plane-web-automation.ts
import { Page } from 'playwright';

class PlaneWebAutomation {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto('http://localhost:3000/sign-in');
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="sign-in-button"]');
    await this.page.waitForURL('**/workspace/*');
  }

  async createIssue(workspaceSlug: string, projectId: string, issueData: {
    title: string;
    description?: string;
    priority?: string;
    assignee?: string;
  }) {
    await this.page.goto(`http://localhost:3000/${workspaceSlug}/projects/${projectId}/issues`);
    await this.page.click('[data-testid="create-issue-button"]');
    
    await this.page.fill('[data-testid="issue-title"]', issueData.title);
    if (issueData.description) {
      await this.page.fill('[data-testid="issue-description"]', issueData.description);
    }
    
    await this.page.click('[data-testid="create-issue-submit"]');
    await this.page.waitForSelector('[data-testid="issue-created-success"]');
  }

  async getIssueList(workspaceSlug: string, projectId: string) {
    await this.page.goto(`http://localhost:3000/${workspaceSlug}/projects/${projectId}/issues`);
    await this.page.waitForSelector('[data-testid="issue-list"]');
    
    const issues = await this.page.$$eval('[data-testid="issue-item"]', items => 
      items.map(item => ({
        title: item.querySelector('[data-testid="issue-title"]')?.textContent,
        status: item.querySelector('[data-testid="issue-status"]')?.textContent,
        assignee: item.querySelector('[data-testid="issue-assignee"]')?.textContent
      }))
    );
    
    return issues;
  }
}
```

### 🔧 **Approach 4: Database Direct Access**

**Advantages:**
- Fastest access to data
- No API limitations
- Can perform complex queries
- Direct access to all data

**Implementation:**
```python
# plane_db_service.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

class PlaneDBService:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            database=os.getenv('POSTGRES_DB', 'plane'),
            user=os.getenv('POSTGRES_USER', 'plane'),
            password=os.getenv('POSTGRES_PASSWORD', 'plane'),
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def get_workspaces(self):
        self.cursor.execute("SELECT * FROM workspaces WHERE deleted_at IS NULL")
        return self.cursor.fetchall()

    def get_projects(self, workspace_id):
        self.cursor.execute("""
            SELECT * FROM projects 
            WHERE workspace_id = %s AND deleted_at IS NULL
        """, (workspace_id,))
        return self.cursor.fetchall()

    def get_issues(self, project_id, filters=None):
        query = """
            SELECT i.*, s.name as state_name, s.color as state_color
            FROM issues i
            LEFT JOIN states s ON i.state_id = s.id
            WHERE i.project_id = %s AND i.deleted_at IS NULL
        """
        params = [project_id]
        
        if filters:
            if filters.get('priority'):
                query += " AND i.priority = %s"
                params.append(filters['priority'])
            if filters.get('state'):
                query += " AND s.name = %s"
                params.append(filters['state'])
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def create_issue(self, issue_data):
        self.cursor.execute("""
            INSERT INTO issues (name, description, priority, project_id, workspace_id, created_at, updated_at)
            VALUES (%(name)s, %(description)s, %(priority)s, %(project_id)s, %(workspace_id)s, NOW(), NOW())
            RETURNING *
        """, issue_data)
        self.connection.commit()
        return self.cursor.fetchone()
```

---

## Configuration and Setup

### **Environment Configuration**
```bash
# .env for Plane integration
PLANE_API_URL=http://localhost:8000
PLANE_API_KEY=your_api_key_here
PLANE_WORKSPACE_SLUG=your-workspace
PLANE_PROJECT_ID=your-project-id

# Database access (if using direct DB approach)
POSTGRES_HOST=localhost
POSTGRES_DB=plane
POSTGRES_USER=plane
POSTGRES_PASSWORD=plane
POSTGRES_PORT=5432
```

### **MCP Configuration**
```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "plane-local": {
      "command": "node",
      "args": ["plane-mcp-server.js"],
      "env": {
        "PLANE_API_URL": "http://localhost:8000",
        "PLANE_API_KEY": "your_plane_api_key"
      }
    }
  }
}
```

### **Authentication Setup**
```typescript
// API Token generation (in Plane admin)
// 1. Go to Settings → API Tokens
// 2. Create new token with appropriate permissions
// 3. Use token in Authorization header: `Bearer ${token}`

class PlaneAuth {
  static async generateAPIToken(email: string, password: string) {
    const response = await fetch('http://localhost:8000/api/sign-in/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    return data.access_token;
  }
}
```

---

## Usage Examples

### **Creating Issues from Cursor**
```typescript
// LLM can use this pattern to create issues
const planeService = new PlaneLLMService();

async function createIssueFromCursor(issueData: {
  title: string;
  description: string;
  priority: string;
  workspace: string;
  project: string;
}) {
  try {
    const issue = await planeService.createIssue(
      issueData.workspace,
      issueData.project,
      {
        name: issueData.title,
        description: issueData.description,
        priority: issueData.priority
      }
    );
    
    console.log(`✅ Created issue: ${issue.name} (${issue.id})`);
    return issue;
  } catch (error) {
    console.error('❌ Failed to create issue:', error);
    throw error;
  }
}
```

### **Project Analytics from Cursor**
```typescript
async function getProjectInsights(workspaceSlug: string, projectId: string) {
  const analytics = await planeService.getProjectAnalytics(workspaceSlug, projectId);
  const issues = await planeService.getIssues(workspaceSlug, projectId);
  
  return {
    totalIssues: issues.length,
    openIssues: issues.filter(i => i.state_detail?.group === 'started').length,
    completedIssues: issues.filter(i => i.state_detail?.group === 'completed').length,
    highPriorityIssues: issues.filter(i => i.priority === 'high').length,
    analytics: analytics
  };
}
```

---

## Best Practices

### **Security Considerations**
- **API Key Management**: Store API keys securely in environment variables
- **Rate Limiting**: Implement rate limiting for API calls
- **Input Validation**: Validate all inputs before sending to Plane API
- **Error Handling**: Implement comprehensive error handling
- **Audit Logging**: Log all LLM interactions with Plane

### **Performance Optimization**
- **Caching**: Cache frequently accessed data
- **Batch Operations**: Use batch APIs when available
- **Connection Pooling**: Use connection pooling for database access
- **Async Operations**: Use async/await for non-blocking operations

### **Integration Patterns**
- **Follow Existing Patterns**: Use established service patterns from the codebase
- **Type Safety**: Use TypeScript interfaces from `packages/types`
- **Error Handling**: Follow existing error handling patterns
- **Logging**: Use the established logging framework

---

## Troubleshooting

### **Common Issues**
- **CORS Errors**: Configure CORS settings in Django settings
- **Authentication Failures**: Verify API key and permissions
- **Network Issues**: Check if Plane is running on correct port
- **Database Connection**: Verify database credentials and connectivity

### **Debugging Tools**
```bash
# Check Plane API health
curl http://localhost:8000/api/health/

# Test authentication
curl -H "Authorization: Bearer your_token" http://localhost:8000/api/workspaces/

# Check database connectivity
psql -h localhost -U plane -d plane -c "SELECT COUNT(*) FROM workspaces;"
```

---

## Conclusion

The **Direct API Integration** approach is recommended for most use cases as it:
- Leverages existing Django REST API
- Provides full functionality access
- Maintains consistency with existing patterns
- Offers the best balance of reliability and features

The MCP Server approach is ideal for native Cursor integration, while web automation and direct database access serve specific use cases where API access is limited or additional functionality is needed. 