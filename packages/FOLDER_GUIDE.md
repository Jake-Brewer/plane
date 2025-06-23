# Packages Directory Guide
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains shared packages and utilities used across the Plane project. It implements a monorepo structure where common functionality is packaged into reusable modules that can be consumed by different applications within the project.

## Scope

### In-Scope
- Shared TypeScript/JavaScript packages
- Common utilities and helper functions
- UI components and design system
- Configuration packages
- Type definitions and interfaces
- Testing utilities and frameworks

### Out-of-Scope
- Application-specific code (see `web/`, `admin/`, `space/`, etc.)
- API server code (see `apiserver/`)
- Deployment configurations (see `deploy/`)
- Documentation (see `docs/`)

## Directory Structure

```
packages/
├── FOLDER_GUIDE.md (This file)
├── constants/          # Shared constants and enums
├── editor/            # Rich text editor components
├── eslint-config/     # ESLint configuration packages
├── hooks/             # Reusable React hooks
├── i18n/              # Internationalization utilities
├── logger/            # Logging utilities and configuration
├── propel/            # Propel-specific utilities
├── services/          # API service layer abstractions
├── shared-state/      # Shared state management utilities
├── tailwind-config/   # Tailwind CSS configuration
├── types/             # TypeScript type definitions
├── typescript-config/ # TypeScript configuration packages
├── ui/                # UI component library
└── utils/             # General utility functions
```

## Package Overview

### Core Packages

#### constants/
- **Purpose**: Shared constants, enums, and configuration values
- **Usage**: Imported across all applications for consistency
- **Key Files**: Various constant definitions organized by domain

#### types/
- **Purpose**: TypeScript type definitions and interfaces
- **Usage**: Provides type safety across the entire project
- **Key Files**: 37+ type definition files organized by domain
- **Structure**: Includes subdirectories for issues/, project/, instance/, cycle/, module/, importer/, favorite/, current-user/, workspace-draft-issues/
- **Coverage**: Comprehensive types for workspace, users, issues, projects, analytics, integrations, and more

#### utils/
- **Purpose**: General utility functions and helpers
- **Usage**: Common functionality used across applications
- **Key Files**: Various utility modules organized by functionality

### UI and Styling

#### ui/
- **Purpose**: Reusable UI component library
- **Usage**: Core components used across all frontend applications
- **Key Files**: 27+ component directories including buttons, forms, modals, tables, icons, dropdowns, etc.
- **Structure**: Organized by component type (avatar/, badge/, button/, card/, dropdown/, form-fields/, modals/, tables/, etc.)
- **Components**: Comprehensive UI library with toast, tooltip, progress, typography, breadcrumbs, and specialized components

#### tailwind-config/
- **Purpose**: Shared Tailwind CSS configuration
- **Usage**: Consistent styling configuration across applications
- **Key Files**: Tailwind configuration and theme definitions

#### propel/
- **Purpose**: Propel-specific UI utilities
- **Usage**: Specialized components and utilities for Propel integration
- **Key Files**: Propel-related components and configurations

### Development Tools

#### eslint-config/
- **Purpose**: Shared ESLint configuration packages
- **Usage**: Consistent code quality standards across project
- **Key Files**: ESLint configurations for different project types

#### typescript-config/
- **Purpose**: Shared TypeScript configuration packages
- **Usage**: Consistent TypeScript compilation settings
- **Key Files**: Base TypeScript configurations for different environments

### Functionality Packages

#### editor/
- **Purpose**: Rich text editor components and utilities
- **Usage**: Provides editing capabilities across applications
- **Key Files**: Editor core, extensions, and utilities

#### hooks/
- **Purpose**: Reusable React hooks
- **Usage**: Common React patterns and state management
- **Key Files**: Various custom hooks organized by functionality

#### services/
- **Purpose**: API service layer abstractions
- **Usage**: Standardized API communication across applications
- **Key Files**: 16+ service directories covering all API domains
- **Structure**: Organized by domain (analytics/, auth/, cycle/, dashboard/, file/, issue/, project/, user/, workspace/, etc.)
- **Coverage**: Complete API service layer with specialized services for AI, developer tools, intake, labels, modules, and states

#### shared-state/
- **Purpose**: Shared state management utilities
- **Usage**: State synchronization across different parts of the application
- **Key Files**: State management utilities and patterns

### Utility Packages

#### i18n/
- **Purpose**: Internationalization utilities and translations
- **Usage**: Multi-language support across applications
- **Key Files**: Translation files and i18n configuration

#### logger/
- **Purpose**: Logging utilities and configuration
- **Usage**: Consistent logging across applications
- **Key Files**: Logger configuration and utilities

## Package Management

### Development Workflow
- **Monorepo Structure**: All packages managed within single repository
- **Dependency Management**: Shared dependencies and version coordination
- **Build System**: Coordinated build process across packages
- **Testing**: Integrated testing across package boundaries

### Package Dependencies
- **Internal Dependencies**: Packages may depend on other packages
- **External Dependencies**: Managed at package and workspace level
- **Version Coordination**: Consistent versioning across related packages
- **Dependency Updates**: Coordinated updates to maintain compatibility

## Usage Guidelines

### Package Consumption
- **Import Patterns**: Consistent import patterns across applications
- **Version Management**: Proper version specification and updates
- **Documentation**: Each package includes usage documentation
- **Examples**: Reference implementations and usage examples

### Package Development
- **Coding Standards**: Follow project-wide coding standards
- **Testing Requirements**: Comprehensive testing for all packages
- **Documentation**: Complete documentation for public APIs
- **Versioning**: Semantic versioning for package releases

## Maintenance

### Regular Tasks
- **Dependency Updates**: Keep external dependencies current
- **Security Audits**: Regular security scanning and updates
- **Performance Monitoring**: Monitor package performance impact
- **Documentation Updates**: Keep documentation current with implementation

### Quality Assurance
- **Code Reviews**: All package changes require review
- **Testing**: Comprehensive test coverage for all packages
- **Performance Testing**: Monitor impact on application performance
- **Compatibility Testing**: Ensure compatibility across all consuming applications

---

**Note**: This directory contains shared packages used across the Plane project. Each package should include its own README.md with specific usage instructions and API documentation. 