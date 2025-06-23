# Project-Specific LLM Primer - Plane
# Last Updated: 2025-01-27T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## Project Identity

### What is Plane
Plane is an open-source project management tool that helps teams track issues, run cycles (sprints), and manage product roadmaps. It's designed to be a comprehensive alternative to tools like Jira, Linear, and Asana.

**Repository**: https://github.com/makeplane/plane  
**Live Demo**: https://app.plane.so  
**Documentation**: https://docs.plane.so

### Project Architecture
Plane is a full-stack application built with:
- **Frontend**: Next.js (React) with TypeScript
- **Backend**: Django REST API with Python
- **Database**: PostgreSQL
- **Cache**: Redis  
- **Deployment**: Docker, Kubernetes
- **Infrastructure**: Multi-container architecture

### Project Structure
```
plane-working/
├── web/           # Next.js frontend application
├── space/         # Public space frontend  
├── admin/         # Admin panel frontend
├── apiserver/     # Django backend API
├── live/          # Real-time collaboration service
├── packages/      # Shared packages and utilities
├── deploy/        # Deployment configurations
├── nginx/         # Reverse proxy configuration
└── for_llm/       # LLM guidance and documentation
```

---

## Current Project Context

### Development Stage
- **Status**: Active development, mature codebase
- **Version**: Production-ready with ongoing feature development
- **Community**: Active open-source community with regular contributions
- **Deployment**: Available as cloud service and self-hosted

### Key Features
- **Issue Management**: Create, track, and manage issues with rich text editor
- **Cycles**: Sprint-like workflow management with burn-down charts  
- **Modules**: Group related issues into modules/projects
- **Views**: Custom filters and saved views for issue organization
- **Pages**: Document creation with AI capabilities
- **Analytics**: Real-time insights and project analytics
- **Drive**: File sharing and document management (coming soon)

### Integration Capabilities
- **GitHub**: Pull request and commit integration
- **Slack**: Notifications and workflow integration  
- **Discord**: Community and team communication
- **Linear**: Migration and synchronization (via our custom integration)
- **Import/Export**: CSV, GitHub, Jira importers

---

## LLM Working Context

### Our Role
We are working on **Linear integration capabilities** for this Plane installation. This includes:
- Setting up Linear API authentication
- Creating project management workflows
- Implementing issue synchronization
- Building cross-platform coordination

### Linear Integration Scope
- **Authentication**: OAuth-based Linear API access
- **Issue Sync**: Bidirectional issue synchronization
- **Project Management**: Linear project management through Plane interface
- **Workflow Automation**: Automated status updates and notifications
- **Cross-References**: Link Plane issues to Linear issues and vice versa

### Current Focus Areas
1. **Project Management**: Implementing Linear-compatible workflows
2. **API Integration**: Robust Linear API connectivity
3. **Documentation**: Maintaining comprehensive guidance for LLM agents
4. **Multi-Agent Coordination**: Supporting collaborative development workflows

---

## Technical Specifications

### Development Environment
- **Languages**: TypeScript, Python, JavaScript
- **Frameworks**: Next.js, Django, React
- **Package Manager**: npm/yarn for frontend, pip for backend
- **Build Tools**: Turbo (monorepo), webpack, vite
- **Testing**: Jest, pytest, Cypress
- **Code Quality**: ESLint, Prettier, Black

### Database Schema
- **Issues**: Core issue tracking with properties, labels, assignees
- **Projects**: Project organization and management
- **Users**: User management and permissions
- **Workspaces**: Multi-tenant workspace organization
- **Cycles**: Sprint/iteration management
- **Modules**: Feature grouping and organization

### API Architecture
- **REST API**: Django REST Framework with comprehensive endpoints
- **Authentication**: JWT-based authentication with OAuth providers
- **Permissions**: Role-based access control (RBAC)
- **Rate Limiting**: API rate limiting and throttling
- **Documentation**: OpenAPI/Swagger documentation

---

## Project-Specific Guidelines

### Code Standards
- **TypeScript First**: All new frontend code in TypeScript
- **Component Architecture**: Reusable component patterns
- **State Management**: Zustand for state management
- **Styling**: Tailwind CSS with custom design system
- **Testing**: Comprehensive test coverage required

### Documentation Requirements
- **API Changes**: Document all API modifications
- **Component Changes**: Update component documentation
- **Configuration**: Maintain deployment configuration docs
- **User Guides**: Keep user-facing documentation current

### Deployment Considerations
- **Docker**: All components containerized
- **Environment Variables**: Comprehensive environment configuration
- **Database Migrations**: Handle migrations carefully
- **Monitoring**: Application performance monitoring
- **Security**: Security-first deployment practices

---

## Linear Integration Specifics

### Authentication Flow
1. **OAuth Setup**: Configure Linear OAuth application
2. **Token Management**: Secure token storage and refresh
3. **Connection Validation**: Regular connection health checks
4. **Error Handling**: Robust error handling and retry logic

### Data Synchronization
- **Issue Mapping**: Map Plane issues to Linear issues
- **Status Synchronization**: Keep status updates synchronized
- **Comment Sync**: Synchronize comments and updates
- **Attachment Handling**: Handle file attachments appropriately

### Workflow Integration
- **Project Creation**: Create projects in both systems
- **Team Management**: Synchronize team member access
- **Label Synchronization**: Keep labels and tags synchronized
- **Milestone Tracking**: Coordinate milestone and deadline tracking

---

## Success Metrics

### Integration Quality
- **API Response Times**: < 500ms for common operations
- **Sync Accuracy**: 99.9% data consistency between systems
- **Error Rate**: < 0.1% failed operations
- **User Experience**: Seamless workflow integration

### Documentation Quality
- **Completeness**: All features documented
- **Accuracy**: Documentation matches implementation
- **Usability**: Clear, actionable instructions
- **Maintenance**: Regular updates and validation

### Development Efficiency
- **Automation**: Minimize manual intervention
- **Error Handling**: Graceful error recovery
- **Performance**: Optimized for common workflows
- **Scalability**: Support for large teams and projects

---

## Project Contacts and Resources

### Key Resources
- **Main Repository**: https://github.com/makeplane/plane
- **Documentation**: https://docs.plane.so
- **Developer Docs**: https://developers.plane.so
- **Community Discord**: https://discord.com/invite/A92xrEGCge
- **Issue Tracker**: https://github.com/makeplane/plane/issues

### Support Channels
- **GitHub Discussions**: Technical questions and feature requests
- **Discord**: Real-time community support
- **GitHub Issues**: Bug reports and feature requests
- **Email**: security@plane.so for security issues

---

## Important Notes

### Security Considerations
- **API Keys**: Never commit API keys or secrets
- **User Data**: Handle user data with care and compliance
- **Authentication**: Use secure authentication practices
- **Data Privacy**: Respect user privacy and data protection

### Performance Considerations
- **API Limits**: Respect Linear API rate limits
- **Caching**: Implement appropriate caching strategies
- **Database**: Optimize database queries and indexing
- **Frontend**: Optimize bundle sizes and loading performance

### Maintenance Requirements
- **Regular Updates**: Keep dependencies updated
- **Security Patches**: Apply security updates promptly
- **Documentation**: Keep documentation current with code
- **Testing**: Maintain comprehensive test coverage

---

**Remember**: This project primer provides Plane-specific context. Always reference the main `_llm_primer.md` for core behavioral standards and the specialized guidance files in `for_llm/` for domain-specific instructions. 