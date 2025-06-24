# Git Usage Guide for LLM Agents
# Last Updated: 2025-01-27T00:00:00Z

## 🚨 CRITICAL GIT STANDARDS

### **ALWAYS Use No-Pager Flag**
All git commands that might use a pager MUST include the `--no-pager` flag to prevent terminal interruptions.

**Correct Format:**
```bash
git --no-pager <command> [options]
```

**Examples:**
```bash
git --no-pager log --oneline -10
git --no-pager branch -r
git --no-pager diff HEAD~1
git --no-pager show HEAD
git --no-pager status
```

**Why This Matters:**
- Prevents terminal paging interruptions
- Ensures commands complete without user interaction
- Maintains automation compatibility
- Follows established project standards

---

## Branch Management

### **Standard Branch Workflow**

#### 1. **Sync with Latest Changes**
```bash
# Fetch all remote changes
git fetch --all

# Check current branch
git --no-pager branch --show-current

# Switch to main development branch
git checkout develop

# Pull latest changes
git pull origin develop
```

#### 2. **Create Feature Branch**
```bash
# Create and switch to feature branch
git checkout -b feature/descriptive-name

# Push to remote and set upstream
git push -u origin feature/descriptive-name
```

#### 3. **Merge Main Into Feature Branch**
```bash
# Switch to feature branch
git checkout feature/descriptive-name

# Merge latest develop into feature
git merge develop

# Push merged changes
git push origin feature/descriptive-name
```

### **Branch Naming Conventions**
- **Features**: `feature/descriptive-name`
- **Fixes**: `fix/issue-description`
- **Chores**: `chore/task-description`
- **Security**: `security/vulnerability-fix`
- **Tests**: `test/test-description`

---

## Quick Reference

### **Most Common Commands**
```bash
# Status and info
git --no-pager status
git --no-pager log --oneline -10
git --no-pager branch -r

# Working with changes
git add .
git commit -m "message"
git push

# Branch operations
git checkout -b feature/name
git merge develop
git push -u origin feature/name

# Syncing
git fetch --all
git pull origin develop
```

---

**Remember**: Always use `git --no-pager <command>` for commands that might use a pager. This is critical for automation and prevents terminal interruptions. 