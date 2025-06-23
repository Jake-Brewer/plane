# For LLM Folder Guide
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This folder contains specialized LLM guidance files that provide detailed instructions for specific technical domains and scenarios. These files are referenced by the main `_llm_primer.md` file and provide comprehensive guidance when LLMs need domain-specific expertise.

## Scope

### In-Scope
- Specialized LLM guidance for specific technical domains
- Detailed operational procedures and best practices
- Authentication and configuration instructions
- Advanced workflows and collaboration patterns

### Out-of-Scope
- General behavioral standards (see `_llm_primer.md`)
- Project-specific overrides (see `_llm_project_primer.md`)
- Analysis and reference materials (see `docs/working_with_llm/`)
- Human-readable documentation (see main documentation)

## File Organization

### Specialized Guidance Files
All files follow the naming pattern `_llm_*.md` or `*.md` for specialized guidance that LLMs access when triggered by specific task types.

### Files in This Directory

#### Core Collaboration and Management
- **`_llm_linear_project_management.md`** (8.1KB, 211 lines)
  - Comprehensive Linear project management guidance
  - Issue management, workflow automation, dependency tracking
  - GitHub integration and cross-reference patterns
  - Team collaboration and progress tracking
  - Advanced features and best practices

- **`_llm_multi-agent_primer.md`** (8.7KB, 220 lines)
  - Multi-agent collaboration coordination
  - Resource management and synchronization strategies
  - Communication frameworks and quality assurance
  - Error handling, recovery procedures
  - Performance optimization and best practices

#### Technical Operations
- **`_llm_extraction_primer.md`** (9.3KB, 235 lines)
  - Component extraction and modularization
  - Directory structure design and dependency management
  - Step-by-step extraction processes
  - Testing strategies and documentation requirements
  - Deployment, packaging, and maintenance procedures

#### Authentication and Integration
- **`LINEAR_API_CREDENTIALS.md`** (11.2KB, 275 lines)
  - Linear API authentication setup and management
  - OAuth and API key configuration
  - Global MCP configuration with 5 connection methods
  - Connection validation and troubleshooting
  - Security best practices and maintenance procedures

#### Documentation Standards
- **`FOLDER_GUIDE.md`** (This file)
  - Catalog of all files in the for_llm directory
  - Purpose and scope definitions
  - Navigation guide for LLMs and humans
  - Maintenance responsibilities

## Navigation Triggers

LLMs are directed to these files based on specific task triggers defined in `_llm_primer.md`:

### 📋 Linear Project Management
**Triggers:** Creating/updating Linear issues, managing project workflows, setting up dependencies, progress tracking
**File:** `_llm_linear_project_management.md`

### 📦 Component Extraction & Modularization  
**Triggers:** Moving code between projects, creating standalone modules, refactoring system architecture, managing dependencies
**File:** `_llm_extraction_primer.md`

### 🤝 Multi-Agent Collaboration
**Triggers:** Coordinating with other AI agents, distributed task execution, shared resource management, conflict resolution
**File:** `_llm_multi-agent_primer.md`

### 🔐 API Authentication
**Triggers:** Linear API access needed, OAuth setup required, connection troubleshooting
**File:** `LINEAR_API_CREDENTIALS.md`

## File Standards

### Header Requirements
All LLM guidance files must include:
- Title with clear domain identification
- Last Updated timestamp in ISO 8601 format
- Prerequisite reference to `_llm_primer.md`
- Clear overview section

### Content Organization
- Logical section hierarchy with clear navigation
- Comprehensive coverage of domain-specific topics
- Step-by-step procedures where applicable
- Best practices and troubleshooting sections
- Cross-references to related files when appropriate

### Maintenance Requirements
- Update timestamp when any content changes
- Maintain comprehensive and current information
- Test all procedures and examples regularly
- Keep cross-references accurate and up-to-date

## Maintenance Responsibilities

### Real-Time Updates
- IMMEDIATELY update files when procedures change
- Update timestamps in headers when modifications are made
- Validate all cross-references when related files change
- Test documented procedures to ensure accuracy

### Quality Assurance
- Ensure all guidance is technically accurate
- Verify examples and code snippets work correctly
- Maintain consistency with established patterns
- Review for clarity and LLM comprehension

### Documentation Lifecycle
- Regular reviews for obsolete information
- Updates based on operational experience
- Integration of lessons learned and improvements
- Coordination with main `_llm_primer.md` navigation

## Integration Points

### Main Navigation
All files are accessed through the navigation map in `_llm_primer.md` with clear trigger conditions and visual indicators.

### Cross-References
Files reference each other where appropriate, maintaining a coherent knowledge network while avoiding circular dependencies.

### External Integration
Files may reference external documentation, configuration files, and operational procedures, but maintain clear boundaries between LLM guidance and human-readable documentation.

---

**Note**: This folder contains specialized guidance for LLM agents. For human-readable analysis and reference materials, see `docs/working_with_llm/`. For general behavioral standards, see `_llm_primer.md` in the project root. 