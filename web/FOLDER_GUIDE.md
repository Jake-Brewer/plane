# Web Directory Guide
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains the main web frontend application for Plane. It provides the primary user interface for project management, issue tracking, team collaboration, and all end-user features of the Plane platform.

## Scope

### In-Scope
- Main web application user interface
- Project management features
- Issue tracking and management
- Team collaboration tools
- User workspaces and settings
- Frontend routing and navigation

### Out-of-Scope
- Admin panel interfaces (see `admin/`)
- Public space interfaces (see `space/`)
- Backend API logic (see `apiserver/`)
- Documentation (see `docs/`)

## Directory Structure

```
web/
├── FOLDER_GUIDE.md (This file)
├── app/                        # Next.js App Router structure
│   ├── [workspaceSlug]/       # Dynamic workspace routing
│   ├── accounts/              # Account management
│   ├── create-workspace/      # Workspace creation
│   ├── installations/         # App installations
│   ├── invitations/           # User invitations
│   ├── onboarding/           # User onboarding flow
│   ├── profile/              # User profile management
│   ├── sign-up/              # User registration
│   ├── workspace-invitations/ # Workspace invitations
│   ├── layout.tsx            # Root layout component
│   ├── error.tsx             # Error boundary
│   └── global-error.tsx      # Global error handler
├── ce/                         # Community Edition components
│   ├── components/           # CE-specific components
│   ├── constants/            # CE constants and configuration
│   ├── helpers/              # CE helper functions
│   ├── hooks/                # CE React hooks
│   ├── layouts/              # CE layout components
│   ├── services/             # CE API services
│   ├── store/                # CE state management
│   └── types/                # CE TypeScript types
├── core/                       # Core application components
│   ├── components/           # Reusable core components (41 dirs)
│   │   ├── account/          # Account management components
│   │   ├── analytics/        # Analytics and reporting components
│   │   ├── api-token/        # API token management
│   │   ├── archives/         # Archive functionality
│   │   ├── auth-screens/     # Authentication screens
│   │   ├── automation/       # Automation features
│   │   ├── command-palette/  # Command palette interface
│   │   ├── common/           # Common shared components
│   │   ├── core/             # Core system components
│   │   ├── cycles/           # Sprint/cycle management
│   │   ├── dashboard/        # Dashboard components
│   │   ├── dropdowns/        # Dropdown components
│   │   ├── editor/           # Rich text editor
│   │   ├── empty-state/      # Empty state illustrations
│   │   ├── estimates/        # Issue estimation
│   │   ├── exporter/         # Data export functionality
│   │   ├── gantt-chart/      # Gantt chart visualization
│   │   ├── global/           # Global UI components
│   │   ├── graphs/           # Chart and graph components
│   │   ├── home/             # Home page components
│   │   ├── icons/            # Icon components
│   │   ├── inbox/            # Inbox functionality
│   │   ├── instance/         # Instance management
│   │   ├── integration/      # External integrations
│   │   ├── issues/           # Issue management
│   │   ├── labels/           # Label management
│   │   ├── modules/          # Module/feature management
│   │   ├── onboarding/       # User onboarding
│   │   ├── page-views/       # Page view components
│   │   ├── pages/            # Page/document management
│   │   ├── profile/          # User profile management
│   │   ├── project/          # Project management
│   │   ├── project-states/   # Project state management
│   │   ├── sidebar/          # Navigation sidebar
│   │   ├── stickies/         # Sticky notes functionality
│   │   ├── ui/               # UI utility components
│   │   ├── user/             # User management
│   │   ├── views/            # Custom view management
│   │   ├── web-hooks/        # Webhook management
│   │   ├── workspace/        # Workspace management
│   │   └── workspace-notifications/ # Workspace notifications
│   ├── constants/            # Application constants (27 files)
│   ├── hooks/                # Core React hooks (40 hooks)
│   ├── layouts/              # Application layouts
│   ├── lib/                  # Core utility libraries
│   ├── local-db/             # Local database utilities
│   ├── services/             # API service layer (46 services)
│   └── store/                # Core state management (18 stores)
├── ee/                         # Enterprise Edition components
│   ├── components/           # EE-specific components
│   ├── constants/            # EE constants and configuration
│   ├── helpers/              # EE helper functions
│   ├── hooks/                # EE React hooks
│   ├── layouts/              # EE layout components
│   ├── services/             # EE API services
│   ├── store/                # EE state management
│   └── types/                # EE TypeScript types
├── helpers/                    # Application helper functions
├── public/                     # Static assets
│   ├── empty-state/          # Empty state illustrations
│   ├── onboarding/           # Onboarding assets
│   ├── workspace/            # Workspace-related assets
│   └── [various assets]      # Icons, images, favicons
├── styles/                     # Global styles and CSS
├── Dockerfile.web             # Production Docker configuration
├── Dockerfile.dev            # Development Docker configuration
└── [configuration files]      # Next.js and build configuration
```

## Key Features

### Project Management
- **Projects**: Create and manage projects with timelines
- **Issues**: Comprehensive issue tracking and management
- **Cycles**: Sprint-like iteration management
- **Modules**: Feature grouping and organization
- **Views**: Custom issue filters and saved views
- **Pages**: Documentation and note-taking

### Team Collaboration
- **Workspaces**: Multi-tenant workspace organization
- **Teams**: Team management and organization
- **Members**: User management and permissions
- **Invitations**: User and workspace invitation system
- **Comments**: Issue and project discussions

### User Experience
- **Dashboard**: Project overview and analytics
- **Search**: Global search across all content
- **Notifications**: Real-time notifications
- **Profile**: User profile and settings management
- **Onboarding**: New user onboarding flow

### Integration Features
- **GitHub**: Git integration for code tracking
- **Import/Export**: Data import from other platforms
- **API Access**: Developer API access
- **Webhooks**: External system integration

## Technical Architecture

### Framework and Technologies
- **Frontend**: Next.js 14+ with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand for client state
- **Components**: Shared component library from `packages/ui`
- **Icons**: Lucide React icon library

### Edition Structure
- **Community Edition (ce/)**: Open-source features
- **Core (core/)**: Shared functionality across editions
- **Enterprise Edition (ee/)**: Premium features and integrations

### Routing and Navigation
- **App Router**: Next.js 13+ App Router for file-based routing
- **Dynamic Routes**: Workspace and project-based routing
- **Protected Routes**: Authentication-protected pages
- **Layouts**: Nested layout system for consistent UI

### State Management
- **Global State**: Zustand stores for application state
- **Local State**: React hooks for component state
- **API State**: SWR/React Query for server state
- **Persistence**: Local storage for user preferences

## Development Workflow

### Local Development
1. **Dependencies**: Install via workspace root (`yarn install`)
2. **Environment**: Configure environment variables
3. **Development Server**: Run Next.js dev server (`yarn dev`)
4. **Type Checking**: TypeScript compilation and checking

### Component Development
- **Design System**: Follow Plane design system guidelines
- **Reusability**: Create reusable components in appropriate directories
- **Testing**: Unit and integration testing for components
- **Documentation**: Document component APIs and usage

### Feature Development
- **Edition Considerations**: Determine CE vs EE feature placement
- **API Integration**: Integrate with backend services
- **State Management**: Implement proper state handling
- **Routing**: Set up appropriate routing for new features

## Build and Deployment

### Build Process
- **TypeScript**: Compile TypeScript to JavaScript
- **Bundle Optimization**: Webpack optimization for production
- **Asset Processing**: Image and asset optimization
- **Environment Variables**: Build-time environment configuration

### Docker Deployment
- **Multi-stage Build**: Optimized Docker images
- **Environment Configuration**: Runtime environment variables
- **Static Asset Serving**: Efficient static asset delivery
- **Health Checks**: Application health monitoring

## Security Considerations

### Authentication and Authorization
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Permission-based feature access
- **Session Management**: Secure session handling
- **Route Protection**: Protected route implementations

### Data Security
- **Input Validation**: Client-side input validation
- **XSS Protection**: Cross-site scripting prevention
- **CSRF Protection**: Cross-site request forgery protection
- **Secure Communication**: HTTPS and secure API calls

## Performance Optimization

### Frontend Performance
- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Component and route lazy loading
- **Bundle Analysis**: Regular bundle size analysis
- **Caching**: Effective caching strategies

### User Experience
- **Loading States**: Proper loading and skeleton states
- **Error Handling**: Graceful error handling and recovery
- **Offline Support**: Progressive web app features
- **Responsive Design**: Mobile-first responsive design

## Maintenance and Quality

### Code Quality
- **TypeScript**: Strict TypeScript configuration
- **ESLint**: Code quality and consistency linting
- **Prettier**: Code formatting and style consistency
- **Testing**: Comprehensive test coverage

### Regular Tasks
- **Dependency Updates**: Keep dependencies current
- **Security Audits**: Regular security vulnerability scanning
- **Performance Monitoring**: Monitor and optimize performance
- **Documentation**: Keep documentation current with features

---

**Note**: This directory contains the main web application for Plane end-users. For administrative interfaces, see the `admin/` directory. For backend API logic, see the `apiserver/` directory. 