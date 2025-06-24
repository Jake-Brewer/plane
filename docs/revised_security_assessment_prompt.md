# Improved Security Assessment Prompt for Local Multi-Agent Deployment

## Context-Specific Security Assessment Request

I need you to conduct a **Local Deployment Security Assessment** for the Plane project management platform. This system will store sensitive project management data in a **local-only, firewall-protected environment** with **multiple LLM agents** accessing it via MCP integration.

## Deployment Specifications

**Environment:**
- Local machine deployment only (no external web access)
- Firewall rules prevent external connections
- NAS backup at Z: drive (RAID 5 configuration)
- Docker container architecture

**Primary Users:**
- Multiple LLM agents in different Cursor instances
- Each agent needs unique identity and role-based access
- Agents should auto-assign work, update progress, add comments
- Work items assigned without progress for X time → return to open status

## Critical Security Concerns (Priority Order)

### 1. **Data Loss & Corruption** ⚠️ **HIGHEST PRIORITY**
- Database persistence and backup strategy
- Volume mounting to NAS for redundancy
- Recovery procedures and data validation
- Container data persistence across restarts

### 2. **Data Extraction & Portability** ⚠️ **HIGH PRIORITY**  
- Ability to export all project data
- Multiple export formats (CSV, JSON, SQL dumps)
- Migration capabilities if needed
- No vendor lock-in scenarios

### 3. **Multi-Agent Access Control** ⚠️ **HIGH PRIORITY**
- Agent authentication and identification
- Role-based project access (single project vs. multiple)
- Work item timeout and reassignment mechanisms
- Prevent agents from blocking work indefinitely

### 4. **Data Integrity Protection** ⚠️ **MEDIUM PRIORITY**
- Protection against intentional damage
- Database transaction safety
- Concurrent access conflict resolution
- Audit trails for agent activities

### 5. **Source Code Completeness** ⚠️ **MEDIUM PRIORITY**
- Ensure all functionality is in source code
- No hidden/compiled dependencies that prevent modification
- Clear separation between open-source and proprietary components

## Assessment Requirements

### Work Organization
1. **Create workspace**: `for_llm/llm_owned_notes/local-security-assessor/`
2. **Track progress**: `llm_todo_local-security-assessment.md`
3. **Chunk strategy**: Use overlapping file ranges (filename:0-2000, filename:1900-4000) 
4. **Component grouping**: Organize by architectural layers (web/, apiserver/, nginx/, etc.)

### Specific Focus Areas
- **Database Configuration**: PostgreSQL persistence, backup automation
- **Container Security**: Non-root users, minimal attack surface
- **API Security**: Authentication, rate limiting, agent session management  
- **File System**: Proper volume mounting, permission management
- **MCP Integration**: Secure agent communication protocol
- **Backup Strategy**: Automated backups to NAS, recovery testing

### Deliverables Required
1. **Risk Assessment Matrix**: Component-by-component risk analysis
2. **Backup Implementation Plan**: NAS integration and automation scripts
3. **Multi-Agent Architecture**: Database schema and API modifications needed
4. **MCP Integration Guide**: How agents should interact with the system
5. **Recovery Procedures**: Step-by-step data recovery documentation
6. **Security Hardening Checklist**: Actionable improvements

## Success Criteria

Answer: **"Can we deploy this locally with enterprise project management data, knowing that:"**
- Data loss risk is minimized through proper backup strategies
- Multiple LLM agents can work efficiently without conflicts
- All data can be extracted if needed
- System is protected from accidental or intentional damage
- All code is modifiable/maintainable

## Output Location
Store your comprehensive assessment in: `docs/local_deployment_security_assessment.md`

Make it **comprehensive within scope** while being **efficient with words** - focus on actionable recommendations rather than theoretical discussions.

Begin with file inventory, then work through each security domain systematically using your chunking approach. 