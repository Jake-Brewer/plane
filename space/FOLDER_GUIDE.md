# Space Directory Guide
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains the public space frontend for Plane. It provides public-facing interfaces for sharing projects, issues, and information with external stakeholders without requiring full Plane access or authentication.

## Scope

### In-Scope
- Public space user interface
- Public project and issue views
- External stakeholder access
- Read-only public interfaces
- Public documentation and pages
- Anonymous user interactions

### Out-of-Scope
- Full project management features (see `web/`)
- Administrative interfaces (see `admin/`)
- Backend API logic (see `apiserver/`)
- Authenticated user workflows

## Directory Structure

```
space/
├── FOLDER_GUIDE.md (This file)
├── app/                        # Next.js App Router structure
│   ├── [workspaceSlug]/       # Dynamic workspace public routing
│   ├── issues/                # Public issue views
│   ├── views/                 # Public project views
│   ├── error.tsx              # Error boundary
│   ├── layout.tsx             # Root layout component
│   ├── not-found.tsx          # 404 error page
│   └── [page files]           # Additional pages
├── ce/                         # Community Edition components
│   ├── components/            # CE-specific public components
│   ├── hooks/                 # CE public hooks
│   └── store/                 # CE public state management
├── core/                       # Core public components
│   ├── components/            # Reusable public components (7 dirs)
│   ├── hooks/                 # Core public React hooks
│   ├── lib/                   # Public utility libraries
│   ├── store/                 # Core public state management
│   └── types/                 # TypeScript type definitions
├── ee/                         # Enterprise Edition components
│   ├── components/            # EE-specific public components
│   ├── hooks/                 # EE public hooks
│   └── store/                 # EE public state management
├── helpers/                    # Public space helper functions
├── public/                     # Static assets
│   ├── 404.svg               # 404 error illustration
│   ├── auth/                 # Authentication assets
│   ├── favicon/              # Favicon files
│   ├── images/               # Public image assets
│   ├── instance/             # Instance branding assets
│   ├── logos/                # Logo assets
│   ├── plane-logos/          # Plane branding
│   ├── project-not-published.svg # Unpublished project illustration
│   └── [other assets]        # Various public assets
├── styles/                     # Global styles
├── Dockerfile.space           # Production Docker configuration
├── Dockerfile.dev            # Development Docker configuration
└── [configuration files]      # Next.js and build configuration
```

## Key Features

### Public Project Access
- **Public Projects**: View published projects without authentication
- **Project Overview**: Public project information and statistics
- **Project Documentation**: Access to public project pages
- **Team Information**: Public team member information

### Public Issue Tracking
- **Issue Views**: Read-only access to public issues
- **Issue Details**: Detailed public issue information
- **Issue Discussions**: Public comments and discussions
- **Issue Search**: Search public issues and content

### Public Pages
- **Documentation**: Public project documentation and pages
- **Knowledge Base**: Public knowledge sharing
- **Announcements**: Public project announcements
- **Status Pages**: Public project status information

### Stakeholder Interface
- **Client Access**: External client project access
- **Vendor Interfaces**: Vendor and contractor access
- **Community Features**: Open-source project community access
- **Public APIs**: Public API documentation and access

## Technical Architecture

### Framework and Technologies
- **Frontend**: Next.js 14+ with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS with Plane design system
- **State Management**: Zustand for public state
- **Components**: Shared components from `packages/ui`
- **Authentication**: Optional authentication for enhanced features

### Public-First Design
- **Performance**: Optimized for public access and SEO
- **Security**: Secure public data access patterns
- **Accessibility**: Full accessibility compliance for public users
- **Mobile-First**: Responsive design for all devices

### Edition Structure
- **Community Edition (ce/)**: Open-source public features
- **Core (core/)**: Shared public functionality
- **Enterprise Edition (ee/)**: Premium public features

## Routing and Access Control

### Public Routes
- **Workspace Access**: `/[workspaceSlug]` - Public workspace views
- **Issue Access**: `/issues/[issueId]` - Public issue views
- **View Access**: `/views/[viewId]` - Public project views
- **Page Access**: Public documentation and pages

### Access Control
- **Published Content**: Only published/public content accessible
- **Permission Checks**: Server-side permission validation
- **Rate Limiting**: API rate limiting for public access
- **Content Filtering**: Automatic filtering of private content

## Development Workflow

### Local Development
1. **Dependencies**: Install via workspace root
2. **Environment**: Configure public-specific environment variables
3. **Development Server**: Run Next.js dev server for space
4. **Public Data**: Test with published/public content

### Component Development
- **Public Components**: Create components in appropriate directories
- **Responsive Design**: Ensure mobile-first responsive design
- **Performance**: Optimize for public access performance
- **SEO**: Implement proper SEO optimization

### Feature Development
- **Public Features**: Focus on read-only, public-accessible features
- **Integration**: Integrate with public APIs and services
- **State Management**: Implement appropriate public state handling
- **Analytics**: Implement public usage analytics

## Security and Privacy

### Public Data Security
- **Data Filtering**: Automatic filtering of private data
- **Permission Validation**: Server-side permission checking
- **Rate Limiting**: Protection against abuse
- **Content Sanitization**: Proper content sanitization

### Privacy Considerations
- **Anonymous Access**: Support for anonymous users
- **Data Minimization**: Minimal data collection for public users
- **Privacy Compliance**: GDPR and privacy regulation compliance
- **Cookie Management**: Minimal cookie usage for public access

## Performance and SEO

### Performance Optimization
- **Static Generation**: Pre-generated static pages where possible
- **Caching**: Aggressive caching for public content
- **CDN**: Content delivery network optimization
- **Bundle Optimization**: Minimal JavaScript bundles

### SEO Optimization
- **Meta Tags**: Proper meta tag implementation
- **Structured Data**: Schema.org structured data
- **Sitemap**: Dynamic sitemap generation
- **Open Graph**: Social media sharing optimization

## Build and Deployment

### Build Process
- **Public Optimization**: Optimized build for public access
- **Static Assets**: Optimized public asset delivery
- **Environment**: Public-specific environment configuration
- **Bundle Analysis**: Regular performance analysis

### Docker Deployment
- **Lightweight Images**: Optimized Docker images for public access
- **Environment Variables**: Public environment configuration
- **Health Checks**: Public endpoint health monitoring
- **Scaling**: Horizontal scaling for public traffic

## Maintenance and Monitoring

### Regular Tasks
- **Performance Monitoring**: Monitor public endpoint performance
- **Security Updates**: Keep public-facing dependencies updated
- **Content Audits**: Regular audit of public content exposure
- **Analytics Review**: Monitor public usage patterns

### Quality Assurance
- **Public Testing**: Test public access scenarios
- **Security Testing**: Regular security testing of public endpoints
- **Performance Testing**: Public endpoint performance testing
- **Accessibility Testing**: Ensure accessibility compliance

---

**Note**: This directory contains the public space interface for Plane. For full project management features, see the `web/` directory. For administrative interfaces, see the `admin/` directory. 