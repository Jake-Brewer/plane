#!/usr/bin/env node

/**
 * Plane MCP Server for Cursor Integration
 * Provides native Cursor integration with Plane project management platform
 * Uses the existing Django REST API for all operations
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');

class PlaneMCPServer {
  constructor() {
    this.server = new Server({
      name: 'plane-mcp-server',
      version: '1.0.0',
      description: 'MCP server for Plane project management integration'
    });
    
    this.baseURL = process.env.PLANE_API_URL || 'http://localhost:8000';
    this.apiKey = process.env.PLANE_API_KEY;
    
    this.setupTools();
    this.setupResources();
  }

  setupTools() {
    // Workspace Management
    this.server.tool('list_workspaces', {
      description: 'List all workspaces accessible to the user',
      parameters: {}
    }, this.listWorkspaces.bind(this));

    this.server.tool('get_workspace', {
      description: 'Get detailed information about a specific workspace',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' }
      }
    }, this.getWorkspace.bind(this));

    // Project Management
    this.server.tool('list_projects', {
      description: 'List all projects in a workspace',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' }
      }
    }, this.listProjects.bind(this));

    this.server.tool('get_project', {
      description: 'Get detailed information about a specific project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' }
      }
    }, this.getProject.bind(this));

    this.server.tool('create_project', {
      description: 'Create a new project in a workspace',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        name: { type: 'string', required: true, description: 'Project name' },
        description: { type: 'string', description: 'Project description' },
        identifier: { type: 'string', description: 'Project identifier (e.g., PROJ)' },
        network: { type: 'number', description: 'Network type: 0=Secret, 2=Public', default: 2 }
      }
    }, this.createProject.bind(this));

    // Issue Management
    this.server.tool('list_issues', {
      description: 'List issues in a project with optional filtering',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' },
        state: { type: 'string', description: 'Filter by state name' },
        priority: { type: 'string', description: 'Filter by priority: urgent, high, medium, low, none' },
        assignee: { type: 'string', description: 'Filter by assignee user ID' },
        labels: { type: 'string', description: 'Filter by label names (comma-separated)' },
        limit: { type: 'number', description: 'Maximum number of issues to return', default: 50 }
      }
    }, this.listIssues.bind(this));

    this.server.tool('get_issue', {
      description: 'Get detailed information about a specific issue',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' },
        issue_id: { type: 'string', required: true, description: 'Issue ID' }
      }
    }, this.getIssue.bind(this));

    this.server.tool('create_issue', {
      description: 'Create a new issue in a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' },
        name: { type: 'string', required: true, description: 'Issue title' },
        description: { type: 'string', description: 'Issue description in HTML or markdown' },
        priority: { type: 'string', description: 'Priority: urgent, high, medium, low, none', default: 'none' },
        state_id: { type: 'string', description: 'State ID for the issue' },
        assignee_ids: { type: 'array', items: { type: 'string' }, description: 'Array of user IDs to assign' },
        label_ids: { type: 'array', items: { type: 'string' }, description: 'Array of label IDs' },
        parent_id: { type: 'string', description: 'Parent issue ID for sub-issues' }
      }
    }, this.createIssue.bind(this));

    this.server.tool('update_issue', {
      description: 'Update an existing issue',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' },
        issue_id: { type: 'string', required: true, description: 'Issue ID' },
        name: { type: 'string', description: 'Issue title' },
        description: { type: 'string', description: 'Issue description' },
        priority: { type: 'string', description: 'Priority: urgent, high, medium, low, none' },
        state_id: { type: 'string', description: 'State ID' },
        assignee_ids: { type: 'array', items: { type: 'string' }, description: 'Array of user IDs' }
      }
    }, this.updateIssue.bind(this));

    // State Management
    this.server.tool('list_states', {
      description: 'List all states in a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' }
      }
    }, this.listStates.bind(this));

    // Label Management
    this.server.tool('list_labels', {
      description: 'List all labels in a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' }
      }
    }, this.listLabels.bind(this));

    this.server.tool('create_label', {
      description: 'Create a new label in a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' },
        name: { type: 'string', required: true, description: 'Label name' },
        color: { type: 'string', description: 'Label color (hex code)', default: '#3b82f6' },
        description: { type: 'string', description: 'Label description' }
      }
    }, this.createLabel.bind(this));

    // Team Management
    this.server.tool('list_members', {
      description: 'List all members in a workspace or project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', description: 'Project ID (optional, for project members)' }
      }
    }, this.listMembers.bind(this));

    // Analytics
    this.server.tool('get_project_analytics', {
      description: 'Get analytics data for a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' }
      }
    }, this.getProjectAnalytics.bind(this));

    // Cycle Management
    this.server.tool('list_cycles', {
      description: 'List all cycles in a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' }
      }
    }, this.listCycles.bind(this));

    this.server.tool('create_cycle', {
      description: 'Create a new cycle in a project',
      parameters: {
        workspace_slug: { type: 'string', required: true, description: 'Workspace slug identifier' },
        project_id: { type: 'string', required: true, description: 'Project ID' },
        name: { type: 'string', required: true, description: 'Cycle name' },
        description: { type: 'string', description: 'Cycle description' },
        start_date: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
        end_date: { type: 'string', description: 'End date (YYYY-MM-DD)' }
      }
    }, this.createCycle.bind(this));
  }

  setupResources() {
    this.server.resource('plane://workspace/{workspace_slug}', {
      description: 'Workspace information and projects',
      mimeType: 'application/json'
    }, this.getWorkspaceResource.bind(this));

    this.server.resource('plane://project/{workspace_slug}/{project_id}', {
      description: 'Project information and issues',
      mimeType: 'application/json'
    }, this.getProjectResource.bind(this));

    this.server.resource('plane://issue/{workspace_slug}/{project_id}/{issue_id}', {
      description: 'Issue details and comments',
      mimeType: 'application/json'
    }, this.getIssueResource.bind(this));
  }

  // Helper method for API requests
  async apiRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API request failed: ${response.status} ${response.statusText}\n${errorText}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Failed to connect to Plane API: ${error.message}`);
    }
  }

  // Workspace Methods
  async listWorkspaces() {
    return await this.apiRequest('/api/workspaces/');
  }

  async getWorkspace(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/`);
  }

  // Project Methods
  async listProjects(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/`);
  }

  async getProject(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/`);
  }

  async createProject(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/`, {
      method: 'POST',
      body: JSON.stringify(params)
    });
  }

  // Issue Methods
  async listIssues(params) {
    const queryParams = new URLSearchParams();
    if (params.state) queryParams.append('state__name', params.state);
    if (params.priority) queryParams.append('priority', params.priority);
    if (params.assignee) queryParams.append('assignees', params.assignee);
    if (params.labels) queryParams.append('labels__name__in', params.labels);
    if (params.limit) queryParams.append('per_page', params.limit.toString());

    const endpoint = `/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/issues/?${queryParams}`;
    return await this.apiRequest(endpoint);
  }

  async getIssue(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/issues/${params.issue_id}/`);
  }

  async createIssue(params) {
    const { workspace_slug, project_id, ...issueData } = params;
    return await this.apiRequest(`/api/workspaces/${workspace_slug}/projects/${project_id}/issues/`, {
      method: 'POST',
      body: JSON.stringify(issueData)
    });
  }

  async updateIssue(params) {
    const { workspace_slug, project_id, issue_id, ...updateData } = params;
    return await this.apiRequest(`/api/workspaces/${workspace_slug}/projects/${project_id}/issues/${issue_id}/`, {
      method: 'PATCH',
      body: JSON.stringify(updateData)
    });
  }

  // State Methods
  async listStates(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/states/`);
  }

  // Label Methods
  async listLabels(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/labels/`);
  }

  async createLabel(params) {
    const { workspace_slug, project_id, ...labelData } = params;
    return await this.apiRequest(`/api/workspaces/${workspace_slug}/projects/${project_id}/labels/`, {
      method: 'POST',
      body: JSON.stringify(labelData)
    });
  }

  // Member Methods
  async listMembers(params) {
    const endpoint = params.project_id 
      ? `/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/members/`
      : `/api/workspaces/${params.workspace_slug}/members/`;
    return await this.apiRequest(endpoint);
  }

  // Analytics Methods
  async getProjectAnalytics(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/analytics/`);
  }

  // Cycle Methods
  async listCycles(params) {
    return await this.apiRequest(`/api/workspaces/${params.workspace_slug}/projects/${params.project_id}/cycles/`);
  }

  async createCycle(params) {
    const { workspace_slug, project_id, ...cycleData } = params;
    return await this.apiRequest(`/api/workspaces/${workspace_slug}/projects/${project_id}/cycles/`, {
      method: 'POST',
      body: JSON.stringify(cycleData)
    });
  }

  // Resource Methods
  async getWorkspaceResource(uri) {
    const workspace_slug = uri.path.split('/')[1];
    const workspace = await this.getWorkspace({ workspace_slug });
    const projects = await this.listProjects({ workspace_slug });
    
    return {
      workspace,
      projects,
      _metadata: {
        resource_type: 'workspace',
        workspace_slug,
        fetched_at: new Date().toISOString()
      }
    };
  }

  async getProjectResource(uri) {
    const [, workspace_slug, project_id] = uri.path.split('/');
    const project = await this.getProject({ workspace_slug, project_id });
    const issues = await this.listIssues({ workspace_slug, project_id, limit: 100 });
    const states = await this.listStates({ workspace_slug, project_id });
    const labels = await this.listLabels({ workspace_slug, project_id });
    
    return {
      project,
      issues,
      states,
      labels,
      _metadata: {
        resource_type: 'project',
        workspace_slug,
        project_id,
        fetched_at: new Date().toISOString()
      }
    };
  }

  async getIssueResource(uri) {
    const [, workspace_slug, project_id, issue_id] = uri.path.split('/');
    const issue = await this.getIssue({ workspace_slug, project_id, issue_id });
    
    return {
      issue,
      _metadata: {
        resource_type: 'issue',
        workspace_slug,
        project_id,
        issue_id,
        fetched_at: new Date().toISOString()
      }
    };
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Plane MCP Server started');
  }
}

// Start the server
if (require.main === module) {
  const server = new PlaneMCPServer();
  server.start().catch(console.error);
}

module.exports = PlaneMCPServer; 