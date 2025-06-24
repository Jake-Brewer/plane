#!/usr/bin/env node

/**
 * Test script for Plane API integration
 * Validates connectivity and basic operations
 */

const PlaneMCPServer = require('./plane-mcp-server');

class PlaneIntegrationTest {
  constructor() {
    this.baseURL = process.env.PLANE_API_URL || 'http://localhost:8000';
    this.apiKey = process.env.PLANE_API_KEY;
    
    if (!this.apiKey) {
      console.error('❌ PLANE_API_KEY environment variable is required');
      process.exit(1);
    }
  }

  async apiRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      ...options.headers
    };

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

  async testConnection() {
    console.log('🔍 Testing Plane API connection...');
    try {
      const response = await this.apiRequest('/api/workspaces/');
      console.log('✅ Successfully connected to Plane API');
      console.log(`📊 Found ${response.length} workspaces`);
      return true;
    } catch (error) {
      console.error('❌ Failed to connect to Plane API:', error.message);
      return false;
    }
  }

  async testWorkspaces() {
    console.log('\n🏢 Testing workspace operations...');
    try {
      const workspaces = await this.apiRequest('/api/workspaces/');
      
      if (workspaces.length === 0) {
        console.log('⚠️  No workspaces found');
        return false;
      }

      const workspace = workspaces[0];
      console.log(`✅ Found workspace: ${workspace.name} (${workspace.slug})`);
      
      // Test workspace details
      const workspaceDetail = await this.apiRequest(`/api/workspaces/${workspace.slug}/`);
      console.log(`✅ Retrieved workspace details for: ${workspaceDetail.name}`);
      
      return workspace;
    } catch (error) {
      console.error('❌ Workspace test failed:', error.message);
      return false;
    }
  }

  async testProjects(workspace) {
    console.log('\n📁 Testing project operations...');
    try {
      const projects = await this.apiRequest(`/api/workspaces/${workspace.slug}/projects/`);
      
      if (projects.length === 0) {
        console.log('⚠️  No projects found in workspace');
        return false;
      }

      const project = projects[0];
      console.log(`✅ Found project: ${project.name} (${project.id})`);
      
      // Test project details
      const projectDetail = await this.apiRequest(`/api/workspaces/${workspace.slug}/projects/${project.id}/`);
      console.log(`✅ Retrieved project details for: ${projectDetail.name}`);
      
      return project;
    } catch (error) {
      console.error('❌ Project test failed:', error.message);
      return false;
    }
  }

  async testIssues(workspace, project) {
    console.log('\n🎫 Testing issue operations...');
    try {
      const issues = await this.apiRequest(`/api/workspaces/${workspace.slug}/projects/${project.id}/issues/`);
      console.log(`✅ Found ${issues.length} issues in project`);
      
      if (issues.length > 0) {
        const issue = issues[0];
        console.log(`✅ Sample issue: ${issue.name} (${issue.id})`);
        
        // Test issue details
        const issueDetail = await this.apiRequest(`/api/workspaces/${workspace.slug}/projects/${project.id}/issues/${issue.id}/`);
        console.log(`✅ Retrieved issue details for: ${issueDetail.name}`);
      }
      
      return true;
    } catch (error) {
      console.error('❌ Issue test failed:', error.message);
      return false;
    }
  }

  async testStates(workspace, project) {
    console.log('\n🔄 Testing state operations...');
    try {
      const states = await this.apiRequest(`/api/workspaces/${workspace.slug}/projects/${project.id}/states/`);
      console.log(`✅ Found ${states.length} states in project`);
      
      if (states.length > 0) {
        const state = states[0];
        console.log(`✅ Sample state: ${state.name} (${state.color})`);
      }
      
      return true;
    } catch (error) {
      console.error('❌ State test failed:', error.message);
      return false;
    }
  }

  async testLabels(workspace, project) {
    console.log('\n🏷️  Testing label operations...');
    try {
      const labels = await this.apiRequest(`/api/workspaces/${workspace.slug}/projects/${project.id}/labels/`);
      console.log(`✅ Found ${labels.length} labels in project`);
      
      if (labels.length > 0) {
        const label = labels[0];
        console.log(`✅ Sample label: ${label.name} (${label.color})`);
      }
      
      return true;
    } catch (error) {
      console.error('❌ Label test failed:', error.message);
      return false;
    }
  }

  async testMCPServer() {
    console.log('\n🔧 Testing MCP Server functionality...');
    try {
      const server = new PlaneMCPServer();
      
      // Test workspace listing
      const workspaces = await server.listWorkspaces();
      console.log(`✅ MCP Server: Found ${workspaces.length} workspaces`);
      
      if (workspaces.length > 0) {
        const workspace = workspaces[0];
        
        // Test project listing
        const projects = await server.listProjects({ workspace_slug: workspace.slug });
        console.log(`✅ MCP Server: Found ${projects.length} projects`);
        
        if (projects.length > 0) {
          const project = projects[0];
          
          // Test issue listing
          const issues = await server.listIssues({ 
            workspace_slug: workspace.slug, 
            project_id: project.id,
            limit: 5
          });
          console.log(`✅ MCP Server: Found ${issues.length} issues`);
        }
      }
      
      return true;
    } catch (error) {
      console.error('❌ MCP Server test failed:', error.message);
      return false;
    }
  }

  async runAllTests() {
    console.log('🚀 Starting Plane Integration Tests\n');
    console.log(`🔗 API URL: ${this.baseURL}`);
    console.log(`🔑 API Key: ${this.apiKey ? '***configured***' : 'NOT SET'}\n`);

    let allPassed = true;

    // Test basic connection
    const connectionOk = await this.testConnection();
    if (!connectionOk) {
      console.log('\n❌ Connection test failed - stopping tests');
      return false;
    }

    // Test workspaces
    const workspace = await this.testWorkspaces();
    if (!workspace) {
      console.log('\n❌ Workspace test failed - stopping tests');
      return false;
    }

    // Test projects
    const project = await this.testProjects(workspace);
    if (!project) {
      console.log('\n❌ Project test failed - stopping tests');
      return false;
    }

    // Test issues
    const issuesOk = await this.testIssues(workspace, project);
    allPassed = allPassed && issuesOk;

    // Test states
    const statesOk = await this.testStates(workspace, project);
    allPassed = allPassed && statesOk;

    // Test labels
    const labelsOk = await this.testLabels(workspace, project);
    allPassed = allPassed && labelsOk;

    // Test MCP Server
    const mcpOk = await this.testMCPServer();
    allPassed = allPassed && mcpOk;

    console.log('\n' + '='.repeat(50));
    if (allPassed) {
      console.log('✅ All tests passed! Plane integration is ready.');
      console.log('\nNext steps:');
      console.log('1. Add the MCP configuration to ~/.cursor/mcp.json');
      console.log('2. Restart Cursor to load the MCP server');
      console.log('3. Start using Plane commands in Cursor conversations');
    } else {
      console.log('❌ Some tests failed. Please check the configuration.');
    }
    console.log('='.repeat(50));

    return allPassed;
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new PlaneIntegrationTest();
  tester.runAllTests()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('💥 Test runner failed:', error);
      process.exit(1);
    });
}

module.exports = PlaneIntegrationTest; 