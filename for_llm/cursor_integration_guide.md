# Cursor Integration Guide for Plane Project
# Last Updated: 2025-01-27T00:00:00Z

## Overview
This guide provides comprehensive instructions for integrating Cursor IDE with the Plane project, including Linear project management, development workflows, and optimization strategies.

## 🎯 Quick Start Checklist

### Essential Files Created
- [x] `.cursorrules` - Project-specific AI rules and patterns
- [x] `.cursor/settings.json` - Cursor IDE configuration
- [x] `plane.code-workspace` - Multi-folder workspace setup
- [x] This integration guide

### Recommended Cursor Setup
1. **Open Workspace**: Use `plane.code-workspace` for multi-folder development
2. **Install Extensions**: Follow recommendations in workspace file
3. **Configure Models**: Claude 4 Sonnet for chat, Claude 3.5 Sonnet for autocomplete
4. **Enable MCP**: Linear integration for project management

## 🚀 Optimal Development Workflow

### Daily Development Routine
```bash
# 1. Open Cursor with workspace
cursor plane.code-workspace

# 2. Start development services
# Use Ctrl+Shift+P > Tasks: Run Task > "🚀 Start All Services"

# 3. Begin development with Linear integration
# Create Linear issue → Start development → Commit with issue reference
```

### Linear Integration Workflow
1. **Issue Creation**: Create Linear issues for all development tasks
2. **Branch Naming**: Use Linear issue ID in branch names (`feature/PLANE-123-add-feature`)
3. **Commit Messages**: Reference Linear issues (`feat: add new feature (PLANE-123)`)
4. **Status Updates**: Update Linear issue status as work progresses

## 🔧 Cursor Configuration Details

### Model Selection Strategy
Based on task complexity and cost considerations (See `for_llm/_llm_model_selection_guide.md` for detailed recommendations):

| Task Type | Primary Model | Fallback Model | Reasoning |
|-----------|---------------|----------------|-----------|
| **Architecture Design** | Claude 4 Sonnet | GPT-4.1 | Best for complex system design |
| **Code Generation** | Claude 3.5 Sonnet | Claude 4 Sonnet | Balanced performance/cost |
| **Documentation** | Claude 3.5 Sonnet | Gemini 2.5 Flash | Excellent for markdown/docs |
| **Debugging** | Claude 4 Sonnet | o1-mini | Superior reasoning for complex bugs |
| **Refactoring** | Claude 3.5 Sonnet | Claude 4 Sonnet | Good at understanding existing code |

**Note**: These recommendations may be adjusted based on User Assigned Points in the model selection guide.

### Context Management
```json
{
  "cursor.context.includePatterns": [
    "**/*.ts", "**/*.tsx", "**/*.py", "**/*.md",
    "**/package.json", "**/requirements.txt",
    "**/*primer*.md", "**/FOLDER_GUIDE.md"
  ],
  "cursor.context.excludePatterns": [
    "**/node_modules/**", "**/dist/**", "**/build/**",
    "**/.git/**", "**/coverage/**", "**/*.log"
  ]
}
```

## 📁 Project Structure Navigation

### Folder Organization for Cursor
```
plane-working/
├── 🏠 Root/                    # Project configuration
├── 🌐 Web App/                 # Main frontend application
├── 🚀 Space App/               # Public space frontend
├── ⚙️ Admin Panel/             # Admin interface
├── 🔧 API Server/              # Django backend
├── ⚡ Live Service/            # Real-time features
├── 📦 Packages/                # Shared libraries
├── 🚀 Deployment/              # Docker/K8s configs
├── 🤖 LLM Guidance/           # AI assistant context
└── 📚 Documentation/          # Project docs
```

### Key Files for AI Context
- `_llm_primer.md` - Core behavioral standards
- `_llm_project_primer.md` - Project-specific context
- `for_llm/*.md` - Specialized guidance files
- `*/FOLDER_GUIDE.md` - Directory navigation aids

## 🎨 Development Patterns

### Component Development Pattern
```typescript
// Recommended structure for Cursor AI assistance
import { FC } from "react";
import { observer } from "mobx-react";
import { useRouter } from "next/router";

interface ComponentProps {
  // Define props with clear types for AI understanding
  id: string;
  title: string;
  onAction?: (id: string) => void;
}

export const Component: FC<ComponentProps> = observer(({ 
  id, 
  title, 
  onAction 
}) => {
  const router = useRouter();
  
  // Clear, descriptive variable names help AI understand context
  const handleClick = () => {
    onAction?.(id);
  };
  
  return (
    <div className="component-container">
      <h2>{title}</h2>
      <button onClick={handleClick}>Action</button>
    </div>
  );
});
```

### API Service Pattern
```typescript
// Service pattern optimized for AI assistance
export class IssueService extends APIService {
  async getIssues(
    workspaceSlug: string,
    projectId: string,
    filters?: IssueFilters
  ): Promise<IssueResponse> {
    return this.get(`/api/workspaces/${workspaceSlug}/projects/${projectId}/issues`, {
      params: filters
    })
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }
}
```

## 🔍 Debugging and Troubleshooting

### Common Cursor Issues
1. **Slow Autocomplete**: Exclude large files from context
2. **Incorrect Suggestions**: Update `.cursorrules` with project patterns
3. **Memory Issues**: Limit concurrent file context
4. **Model Limits**: Switch to appropriate model for task complexity

### Debug Configuration
```json
{
  "name": "🐍 Debug Django API",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/apiserver/manage.py",
  "args": ["runserver", "0.0.0.0:8000", "--noreload"],
  "django": true,
  "cwd": "${workspaceFolder}/apiserver"
}
```

## 🚀 Performance Optimization

### Cursor Performance Tips
1. **Selective Context**: Only include relevant files in context
2. **Model Selection**: Use appropriate model for task complexity
3. **Workspace Organization**: Use multi-folder workspace for large projects
4. **Extension Management**: Only install necessary extensions

### Memory Management
```json
{
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/.mypy_cache/**": true
  }
}
```

## 🔐 Security Considerations

### Environment Variables
```bash
# .env.local (never commit)
LINEAR_API_KEY=your_linear_api_key
CURSOR_API_KEY=your_cursor_api_key
DATABASE_URL=postgresql://...
```

### Secure Development
- Use environment variables for sensitive data
- Never commit API keys or credentials
- Use secure authentication patterns
- Validate all user inputs
- Follow OWASP security guidelines

## 📊 Monitoring and Analytics

### Development Metrics
- **Code Quality**: ESLint, Prettier, TypeScript strict mode
- **Performance**: Bundle size, API response times
- **Testing**: Unit test coverage, integration tests
- **Security**: Security scanning, dependency audits

### Linear Integration Metrics
- **Issue Tracking**: Linear issue completion rates
- **Development Velocity**: Story points per sprint
- **Code Quality**: Review feedback and bug rates
- **Team Productivity**: Cycle time and lead time

## 🎯 Best Practices Summary

### For Cursor AI
1. **Clear Context**: Provide clear, descriptive code comments
2. **Consistent Patterns**: Follow established project patterns
3. **Type Safety**: Use TypeScript for better AI understanding
4. **Documentation**: Maintain up-to-date documentation
5. **Testing**: Write tests for AI-generated code

### For Linear Integration
1. **Issue Tracking**: Create issues for all development work
2. **Branch Naming**: Use consistent branch naming conventions
3. **Commit Messages**: Include Linear issue references
4. **Status Updates**: Keep Linear issues updated
5. **Documentation**: Link code changes to Linear issues

## 🆘 Troubleshooting Guide

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow AI responses | Large context | Reduce included files |
| Incorrect suggestions | Outdated rules | Update `.cursorrules` |
| Linear sync issues | API credentials | Check `LINEAR_API_CREDENTIALS.md` |
| Build failures | Dependency issues | Run `yarn install` |
| Type errors | Missing types | Check `packages/types/` |

### Emergency Procedures
1. **Backup**: Always backup before major changes
2. **Rollback**: Use git to rollback problematic changes
3. **Support**: Check Linear integration documentation
4. **Recovery**: Follow emergency procedures in `_llm_primer.md`

## 📚 Additional Resources

### Documentation Links
- [Cursor Documentation](https://docs.cursor.sh/)
- [Linear API Documentation](https://developers.linear.app/)
- [Plane Documentation](https://docs.plane.so/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Django Documentation](https://docs.djangoproject.com/)

### Learning Resources
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Docker Documentation](https://docs.docker.com/)

---

**Note**: This guide should be updated as the project evolves and new Cursor features become available. Always refer to the latest documentation and best practices. 