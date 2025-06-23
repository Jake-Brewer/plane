# Admin Directory Guide  
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains the admin panel frontend application for Plane. It provides administrative interfaces for managing instance settings, user accounts, authentication providers, and system configuration.

## Scope

### In-Scope
- Admin panel user interface components
- Instance administration features
- Authentication provider configuration
- System settings and configuration management
- Administrative workflows and tools

### Out-of-Scope
- End-user project management interfaces (see `web/`)
- Public space interfaces (see `space/`)
- Backend API logic (see `apiserver/`)
- Documentation (see `docs/`)

## Directory Structure

```
admin/
├── FOLDER_GUIDE.md (This file)
├── app/                    # Next.js application structure
│   ├── ai/                # AI-related admin features
│   ├── authentication/    # Auth provider configuration
│   ├── email/            # Email configuration
│   ├── general/          # General settings
│   ├── image/            # Image management
│   ├── workspace/        # Workspace administration
│   ├── layout.tsx        # Root layout component
│   └── globals.css       # Global styles
├── ce/                    # Community Edition components
├── core/                  # Core admin components and utilities
│   ├── components/       # Reusable admin components
│   │   ├── admin-sidebar/    # Admin navigation sidebar
│   │   ├── authentication/  # Authentication components
│   │   ├── common/          # Common admin components
│   │   ├── instance/        # Instance management components
│   │   ├── login/           # Login interface components
│   │   └── workspace/       # Workspace admin components
│   ├── hooks/           # Admin-specific React hooks
│   ├── layouts/         # Admin layout components
│   ├── lib/             # Admin utility libraries
│   └── store/           # Admin state management
├── ee/                    # Enterprise Edition components
├── public/               # Static assets
│   ├── auth/            # Authentication-related assets
│   ├── favicon/         # Favicon files
│   ├── images/          # Image assets
│   ├── instance/        # Instance-related assets
│   ├── logos/           # Logo assets
│   └── plane-logos/     # Plane branding assets
├── Dockerfile.admin      # Production Docker configuration
├── Dockerfile.dev       # Development Docker configuration
└── [configuration files] # Next.js and build configuration
```

## Key Features

### Instance Administration
- **Instance Settings**: Global instance configuration
- **License Management**: Enterprise license administration
- **System Health**: Instance monitoring and diagnostics
- **Maintenance Mode**: Instance maintenance controls

### User Management
- **User Accounts**: User administration and management
- **Role Assignment**: System-wide role management
- **Access Control**: Permission and access management
- **Account Lifecycle**: User onboarding and offboarding

### Authentication Configuration
- **OAuth Providers**: GitHub, GitLab, Google OAuth setup
- **SAML Integration**: Enterprise SAML configuration
- **Security Settings**: Authentication security policies
- **Session Management**: Session configuration and control

### System Configuration
- **Email Settings**: SMTP and email configuration
- **Image Storage**: Image upload and storage settings
- **AI Integration**: AI service configuration
- **Feature Flags**: Feature enablement and configuration

## Technical Details

### Framework and Technologies
- **Frontend**: Next.js with TypeScript and React
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand for admin state
- **Components**: Shared component library from `packages/ui`
- **API Integration**: Integration with Django backend

### Build Configuration
- **Development**: Hot reload with Next.js dev server
- **Production**: Optimized build with Docker containerization
- **Dependencies**: Shared packages from monorepo
- **Environment**: Environment-specific configuration

### Deployment
- **Docker**: Containerized deployment with multi-stage builds
- **Environment Variables**: Configuration via environment variables
- **Static Assets**: Optimized asset delivery
- **Routing**: Next.js App Router for navigation

## Development Workflow

### Local Development
1. **Dependencies**: Install dependencies via workspace root
2. **Environment**: Configure environment variables
3. **Development Server**: Run Next.js development server
4. **Hot Reload**: Automatic reload on file changes

### Component Development
- **Component Library**: Use shared components from `packages/ui`
- **Admin Components**: Create admin-specific components in `core/components`
- **Layouts**: Utilize admin layout system
- **Hooks**: Use admin-specific hooks for state and API integration

### Integration Points
- **API Backend**: Integration with Django backend in `apiserver/`
- **Shared Packages**: Dependencies on monorepo packages
- **Authentication**: Integration with authentication systems
- **Configuration**: Runtime configuration management

## Security Considerations

### Access Control
- **Admin Permissions**: Strict admin-only access control
- **Role Verification**: Server-side role verification
- **Session Security**: Secure session management
- **CSRF Protection**: Cross-site request forgery protection

### Data Protection
- **Sensitive Data**: Secure handling of configuration data
- **Environment Variables**: Secure environment variable management
- **API Security**: Secure API communication
- **Audit Logging**: Administrative action logging

## Maintenance

### Regular Tasks
- **Security Updates**: Keep dependencies updated for security
- **Performance Monitoring**: Monitor admin panel performance
- **Feature Updates**: Add new administrative features
- **Documentation**: Keep documentation current with features

### Quality Assurance
- **Testing**: Comprehensive testing of admin features
- **Code Reviews**: Review all administrative code changes
- **Security Audits**: Regular security assessment
- **Performance Testing**: Monitor and optimize performance

---

**Note**: This directory contains the admin panel for Plane instance administration. For end-user interfaces, see the `web/` directory. For backend API logic, see the `apiserver/` directory. 