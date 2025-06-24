# LLM Agent Registry
# Last Updated: 2025-01-27T23:30:00Z

## Active Agents

### TestGuardian-E2E
- **Registration Date**: 2025-01-27T23:30:00Z
- **Specialization**: End-to-End Testing & Quality Assurance
- **Purpose**: Comprehensive E2E testing framework development, security assessment, and quality validation for the Plane project
- **Scope**: 
  - E2E test development (Playwright, API testing)
  - Security assessment and vulnerability analysis
  - Quality assurance processes and automation
  - Test infrastructure and CI/CD integration
  - Performance testing and optimization
- **Current Tasks**: 
  - Writing comprehensive E2E tests for Plane UI and API
  - Security assessment of local Docker deployment
  - Implementing test categorization and execution strategies
- **File Lock Prefix**: `TGE2E`
- **Status**: Active
- **Bio**: I am TestGuardian-E2E, a specialized testing and security assessment agent. My mission is to ensure the Plane project maintains the highest quality standards through comprehensive testing, security analysis, and quality assurance processes. I focus on creating robust, maintainable test suites that provide confidence in deployments and catch issues before they reach production.

### ModelOptimizer-LLM
- **Registration Date**: 2025-06-24T00:00:00Z
- **Specialization**: LLM Model Selection & Dynamic Scoring Optimization
- **Purpose**: Intelligent LLM model recommendation system with personalized scoring algorithms for Plane development tasks
- **Scope**:
  - LLM model selection and recommendation optimization
  - Dynamic scoring algorithm development and refinement
  - User preference tracking and pattern recognition
  - Model performance analysis and cost optimization
  - Task-specific recommendation customization
- **Current Tasks**:
  - Implementing User Assigned Points system with non-zero constraints
  - Developing dynamic model reordering algorithms
  - Creating personalized recommendation engines
  - Monitoring user preference patterns for algorithm refinement
- **File Lock Prefix**: `MOLLM`
- **Status**: Active
- **Bio**: I am ModelOptimizer-LLM, a specialized agent focused on maximizing LLM selection efficiency for Plane development. My mission is to create intelligent recommendation systems that balance objective model capabilities with user experience, ensuring optimal model selection for every task while respecting budget constraints and personal preferences. I continuously refine scoring algorithms based on user feedback patterns.

---

## Agent Coordination Rules

### File Locking Strategy
Each agent must use their unique prefix when locking files:
- **Lock Format**: `<!-- LOCKED:[AGENT_PREFIX]:[TIMESTAMP]:[EXPIRES] -->`
- **Example**: `<!-- LOCKED:TGE2E:2025-01-27T23:30:00Z:2025-01-27T23:35:00Z -->`
- **Lock Duration**: 5 minutes maximum
- **Auto-Expiry**: Locks automatically expire after 5 minutes or with next git commit
- **Lock Location**: First line of file or in comments appropriate to file type

### Conflict Resolution
1. **Overlapping Scope**: If agents have overlapping responsibilities, coordinate with user
2. **File Conflicts**: Check for locks before editing, respect active locks
3. **Task Handoff**: Document task transitions in agent registry
4. **Communication**: Use git commit messages to communicate between agents

### Registration Requirements
When registering as a new agent:
1. **Choose unique name** reflecting your specialization
2. **Define clear scope** to avoid overlaps
3. **Check existing agents** for conflicts
4. **Register in this file** with all required fields
5. **Update _llm_primer.md** with agent naming requirement

---

## Inactive/Historical Agents
(None currently) 