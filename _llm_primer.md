# LLM Primer - Core Behavioral Standards
# Last Updated: 2025-01-27T00:00:00Z

## 🚨 PRIMER HIERARCHY - CRITICAL

**READ THIS COMPLETELY AT THE START OF EVERY PROMPT**

### Agent Identity Requirement
**MANDATORY**: Every LLM agent must establish a unique identity before beginning work:
1. **Choose a unique name** that reflects your specialization (e.g., TestGuardian-E2E, DataArchitect-DB, SecurityAuditor-Infra)
2. **Register in** `for_llm/_llm_agent_registry.md` with full details (purpose, scope, bio)
3. **Check for conflicts** with existing agents and resolve with user if needed
4. **Use your agent prefix** for file locking (see registry for format)

This file contains essential behavioral standards needed for every interaction. For specialized knowledge, navigate to the appropriate for_llm/*.md file as indicated below.

### Navigation Map
- **Agent Registry** → `for_llm/_llm_agent_registry.md`
- **Model Selection** → `for_llm/_llm_model_selection_guide.md`
- **Linear Integration** → `for_llm/_llm_linear_project_management.md`
- **Component Extraction** → `for_llm/_llm_extraction_primer.md`
- **Multi-Agent Tasks** → `for_llm/_llm_multi-agent_primer.md`
- **API Authentication** → `for_llm/LINEAR_API_CREDENTIALS.md`

---

## Core Identity & Behavioral Standards

### Primary Identity
You are an AI assistant working on project management and development tasks with Linear project management integration.

### Fundamental Principles
1. **Accuracy First**: Never provide incorrect information
2. **Context Awareness**: Always consider project scope and current state
3. **Proactive Assistance**: Anticipate needs and suggest improvements
4. **Documentation Standards**: Maintain clear, consistent documentation
5. **Safety Protocols**: Follow security best practices

### Critical Safety Rules (NEVER VIOLATE)
- **NEVER DELETE**: _llm_primer.md must remain in project root
- **NEVER MOVE**: Core guidance files maintain their locations
- **BACKUP FIRST**: Always backup before major configuration changes
- **VERSION CONTROL**: All changes must be committed to git
- **PROTECTED FILES**: Treat all _llm*.md files as protected resources

---

## Project Structure Overview

### Multi-Project Ecosystem
1. **docker-command-center** (Current): Project management and development utilities
2. **Related Projects**: Game engine evaluation (parent project)
3. **Global Configuration**: Linear integration available across ALL Cursor projects
4. **Cross-Project Coordination**: Maintain separation of concerns

### File Organization
```
docker-command-center/
├── _llm_primer.md (This file - READ EVERY PROMPT)
├── _llm_project_primer.md (Project-specific context)
├── for_llm/ (Specialized guidance)
│   ├── _llm_extraction_primer.md
│   ├── _llm_multi-agent_primer.md
│   ├── _llm_linear_project_management.md
│   └── LINEAR_API_CREDENTIALS.md
└── docs/working_with_llm/ (Analysis and reference materials)
```

---

## Essential Standards for Every Task

### File Management
- **Naming**: Use descriptive, human-readable names
- **Timestamps**: Include "Last Updated" headers in guidance files
- **Documentation**: Create FOLDER_GUIDE.md in every directory
- **Todo Files**: Use format `for_llm_todo_<agent-name>.md`
- **File Locking**: Always check for and respect file locks before editing:
  - **Check for locks**: Look for `<!-- LOCKED:[AGENT]:[TIME]:[EXPIRES] -->` at file start
  - **Respect active locks**: Do not edit files locked by other agents unless expired
  - **Create locks**: Add lock comment when editing shared files
  - **Lock format**: `<!-- LOCKED:[YOUR_PREFIX]:[ISO_TIMESTAMP]:[EXPIRES_TIMESTAMP] -->`
  - **Auto-expiry**: Locks expire after 5 minutes or with next git commit

### Version Control Protocol
1. **Always backup** before major changes
2. **Commit regularly** with descriptive messages
3. **Never delete** protected files (_llm*.md)
4. **Document changes** in commit messages
5. **Git commands**: Always use `--no-pager` flag to prevent paging interruptions (e.g., `git log --no-pager`)

#### Branch Management Strategy
**CRITICAL**: Never work directly on master or main branches
- **Always create feature branches** from develop: `git checkout -b feature/your-feature-name origin/develop`
- **Merge from develop regularly** to stay current: `git merge origin/develop --no-edit`
- **Push feature branches** to origin for backup: `git push origin feature/your-feature-name`
- **Coordinate with other workers** by keeping branches synced with latest develop changes
- **Branch naming**: Use descriptive prefixes (feature/, bugfix/, security/, refactor/)

### Command Execution Standards
**CRITICAL: All commands must be non-interactive, have appropriate timeouts, and use watchdog monitoring**

#### Command Watchdog System
**MANDATORY**: All terminal commands must be executed with built-in timeout protection:

- **Default Timeout**: 30 seconds for most commands
- **Extended Timeout**: 120 seconds for build/install operations  
- **Long Operations**: 300 seconds for Docker builds, large downloads
- **Background Services**: Use `is_background: true` with no timeout
- **Timeout Behavior**: Commands exceeding timeout automatically terminate with error message

#### Timeout Override System
**CRITICAL**: Agents can request longer timeouts for specific operations:

**Override Syntax**: When requesting longer timeouts, specify in command explanation:
- `"explanation": "Docker build requires 600s timeout - building complex multi-stage image"`
- `"explanation": "Yarn install needs 180s timeout - installing 200+ packages"`
- `"explanation": "Database migration requires 900s timeout - processing 1M+ records"`

**Timeout Override Categories**:
```bash
# Emergency overrides (up to 1800s = 30 minutes)
docker-compose build --no-cache           # 600-1800s for complex builds
yarn install --network-timeout 500000     # 180-600s for large package sets
npm install --yes                         # 120-300s for package installation
database migrations                       # 300-1800s depending on data size

# When to request overrides:
# - Docker builds with multiple stages
# - Package installations with 100+ dependencies  
# - Database operations on large datasets
# - File downloads over 100MB
# - Complex compilation processes
```

#### Yarn Install Whitelisting
**CRITICAL**: Yarn/NPM installs are REQUIRED for development:
- **Registry Access**: registry.yarnpkg.com and registry.npmjs.org are WHITELISTED
- **Package Downloads**: Well-known packages from official registries are allowed
- **Security Monitoring**: All package downloads are logged but not blocked
- **Timeout Requirements**: Use 180-600s timeouts for large package installations

#### Timeout Recovery Procedures
**When a command times out:**
1. **Analyze the cause**: Check if operation legitimately needs more time
2. **Request longer timeout**: Use override syntax with specific reasoning
3. **Break into smaller steps**: Consider chunking large operations
4. **Use background mode**: For services that run indefinitely
5. **Verify prerequisites**: Ensure dependencies are available

**Example Timeout Recovery**:
```bash
# If yarn install times out:
# 1. Check network connectivity
# 2. Verify package.json validity  
# 3. Request 300s timeout with explanation
# 4. Consider using --network-timeout flag
# 5. Check for package registry accessibility
```

#### Interactive Prompt Prevention
- **NPM/NPX**: Always use `--yes` flag (e.g., `npx create-next-app --yes`, `npm install --yes`)
- **Package Managers**: Use non-interactive flags (`--assume-yes`, `--non-interactive`, `--quiet`)
- **Git**: Use `--no-pager` to prevent paging (e.g., `git log --no-pager`, `git diff --no-pager`)
- **Git Branch Info**: Use `git status --porcelain` and `git branch --show-current` instead of `git branch -a`
- **Docker**: Use `--non-interactive` and `--quiet` flags where available
- **General Rule**: Research and use non-interactive flags for ANY command that might prompt for user input

#### Safe Git Command Alternatives
```bash
# AVOID: git branch -a (can hang waiting for pager)
# USE INSTEAD:
git branch --show-current                    # Current branch name
git status --porcelain                       # Clean status check
git log --oneline --no-pager -10            # Recent commits
git remote -v                                # Remote information
git branch -r | Select-Object -First 10     # PowerShell: Remote branches (limited)

# AVOID: git log --oneline -5 (can hang waiting for pager input)
# USE INSTEAD:
git log --oneline --no-pager -n 5           # ALWAYS use -n flag with --no-pager
git log --oneline --no-pager -n 20          # Limited recent history
git show --no-pager HEAD                     # Latest commit details

# AVOID: git diff (can hang in pager)  
# USE INSTEAD:
git diff --no-pager --stat                  # Summary of changes
git diff --no-pager --name-only             # Just file names

# CRITICAL: git branch commands that don't support --no-pager
# AVOID: git branch -r --no-pager (invalid option)
# USE INSTEAD:
git branch -r | Select-String "pattern" | Select-Object -First 10  # PowerShell
git branch -r | head -10                     # Bash/Linux
```

#### Command Validation & Follow-up
1. **Read Command Output**: Always analyze command output to verify expected results
2. **Silent Commands**: Some commands produce no output on success - verify with follow-up commands:
   - After `git commit`: Run `git status --porcelain` to verify clean state
   - After file operations: Use `ls -la` or equivalent to verify file existence/permissions
   - After service starts: Check with `curl` or `ping` to verify service is responding
3. **Expected vs Actual**: Compare actual output with expected patterns
4. **Error Detection**: Look for error codes, "error:" text, or unexpected output patterns
5. **Timeout Recovery**: If command times out, investigate with shorter diagnostic commands

#### Watchdog Implementation Pattern
```bash
# For any command that might hang:
# 1. Set appropriate timeout based on operation type
# 2. Use non-interactive flags
# 3. Have fallback diagnostic commands ready
# 4. Monitor for expected output patterns

# Example: Instead of risky git branch -a
git branch --show-current  # Quick, safe, informative
git remote -v             # Shows remote info without paging risk
```

### Quality Assurance
- **Test before deploy**: Validate all changes
- **Document everything**: Keep docs current with code
- **Follow patterns**: Use established conventions
- **Monitor health**: Check system status regularly

---

## Task-Specific Navigation Guide

### When to Access Specialized Guidance

#### 🤖 Model Selection & Optimization
**Access:** `for_llm/_llm_model_selection_guide.md`
**Triggers:**
- Choosing the right LLM for specific tasks
- Budget optimization for model usage
- Task-specific model recommendations
- Performance vs cost analysis
- Updating User Assigned Points

#### 📋 Linear Project Management
**Access:** `for_llm/_llm_linear_project_management.md`
**Triggers:**
- Creating/updating Linear issues
- Managing project workflows
- Setting up dependencies
- Progress tracking

#### 📦 Component Extraction & Modularization
**Access:** `for_llm/_llm_extraction_primer.md`
**Triggers:**
- Moving code between projects
- Creating standalone modules
- Refactoring system architecture
- Managing dependencies

#### 🤝 Multi-Agent Collaboration
**Access:** `for_llm/_llm_multi-agent_primer.md`
**Triggers:**
- Coordinating with other AI agents
- Distributed task execution
- Shared resource management
- Conflict resolution

#### 🔐 API Authentication
**Access:** `for_llm/LINEAR_API_CREDENTIALS.md`
**Triggers:**
- Linear API access needed
- OAuth setup required
- Connection troubleshooting

---

## Critical Instructions

### Protected File Policy
These files are **PROTECTED** and must never be deleted or moved:
- `_llm_primer.md` (this file)
- `_llm_project_primer.md`
- All files in `for_llm/` directory

### Before Making Changes
1. **Create backup** of affected files
2. **Commit current state** to version control
3. **Test changes** in isolated environment
4. **Update documentation** to reflect changes
5. **Validate** all references still work

### Emergency Procedures
If something goes wrong:
1. **Stop immediately** - don't make it worse
2. **Check git status** - what changed?
3. **Restore from backup** if necessary
4. **Document the issue** for future prevention
5. **Update procedures** to prevent recurrence

---

## Integration Points

### Linear Integration
- **Authentication**: OAuth-based connection (see LINEAR_API_CREDENTIALS.md)
- **Project Tracking**: All work items tracked in Linear
- **Cross-References**: Link Linear issues to GitHub/codebase
- **Status Sync**: Keep Linear and codebase synchronized

### Development Workflow
- **Issue Management**: Track work items in Linear
- **Progress Tracking**: Monitor project completion
- **Documentation**: Maintain clear project documentation
- **Quality Assurance**: Follow testing and validation procedures

---

## Quick Reference

### Most Common Tasks
1. **Linear Issues** → Read `for_llm/_llm_linear_project_management.md`
2. **Code Extraction** → Read `for_llm/_llm_extraction_primer.md` 
3. **Multi-Agent Work** → Read `for_llm/_llm_multi-agent_primer.md`

### Emergency Contacts
- **Protected Files**: NEVER delete _llm*.md files
- **Backup Location**: Version control (git)
- **Rollback Procedure**: `git restore <file>` or restore from backup

---

**Remember**: This primer file is the foundation for all LLM interactions. The specialized guidance in `for_llm/` provides detailed instructions for specific domains. Always read this file completely, then navigate to relevant specialized guidance as needed.