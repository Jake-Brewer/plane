# Component Extraction & Modularization Guide
# Last Updated: 2025-01-27T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## Overview

This guide provides comprehensive instructions for extracting components, moving code between projects, and creating modular, reusable systems. Component extraction is critical for maintaining clean architecture and enabling code reuse across projects.

---

## Extraction Planning

### Pre-Extraction Assessment
1. **Dependency Analysis**: Map all dependencies and interdependencies
2. **Scope Definition**: Clearly define what will be extracted
3. **Interface Design**: Plan clean interfaces between components
4. **Testing Strategy**: Define how extracted components will be tested
5. **Migration Path**: Plan the step-by-step extraction process

### Extraction Criteria
- **Reusability**: Component will be used in multiple contexts
- **Independence**: Component can function with minimal dependencies
- **Cohesion**: Related functionality is grouped together
- **Maintainability**: Component can be maintained independently
- **Performance**: Extraction doesn't negatively impact performance

---

## Directory Structure Design

### Standard Structure Template
```
extracted-component/
├── README.md                    # Component overview and usage
├── CHANGELOG.md                 # Version history and changes
├── _llm_primer.md              # LLM guidance (exact copy from parent)
├── src/                        # Source code
│   ├── __init__.py            # Package initialization
│   ├── core/                  # Core functionality
│   ├── utils/                 # Utility functions
│   └── interfaces/            # External interfaces
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test data and fixtures
├── docs/                       # Documentation
│   ├── api/                   # API documentation
│   ├── examples/              # Usage examples
│   └── architecture/          # Architecture documentation
├── config/                     # Configuration files
│   ├── config.example.json   # Configuration template
│   └── requirements.txt       # Dependencies
└── scripts/                    # Utility scripts
    ├── setup.py              # Installation script
    └── test.py               # Test runner
```

### Naming Conventions
- **Descriptive Names**: Use clear, descriptive names for all components
- **Consistent Patterns**: Follow established naming patterns
- **Version Indicators**: Include version information where appropriate
- **Namespace Clarity**: Avoid naming conflicts with existing components

---

## Dependency Management

### Dependency Mapping
1. **Internal Dependencies**: Dependencies within the same project
2. **External Dependencies**: Third-party libraries and packages
3. **Cross-Project Dependencies**: Dependencies on other projects
4. **System Dependencies**: Operating system and runtime dependencies

### Dependency Minimization
- **Core Dependencies Only**: Include only essential dependencies
- **Optional Dependencies**: Make non-critical dependencies optional
- **Version Pinning**: Pin dependency versions for stability
- **Regular Updates**: Keep dependencies up to date
- **Security Scanning**: Regularly scan for security vulnerabilities

### Interface Design
- **Clean APIs**: Design simple, intuitive interfaces
- **Backward Compatibility**: Maintain compatibility across versions
- **Error Handling**: Implement comprehensive error handling
- **Documentation**: Document all public interfaces
- **Testing**: Test all interface functionality

---

## Extraction Process

### Step-by-Step Extraction
1. **Preparation Phase**
   - Create target directory structure
   - Set up version control for extracted component
   - Document current state and extraction plan
   - Identify all code to be extracted

2. **Code Migration Phase**
   - Copy code to new location
   - Update import statements and references
   - Adapt code to new structure
   - Remove dependencies on parent project

3. **Integration Phase**
   - Update parent project to use extracted component
   - Test integration between parent and extracted component
   - Verify all functionality still works
   - Update documentation and references

4. **Validation Phase**
   - Run comprehensive test suite
   - Validate performance characteristics
   - Check for memory leaks or resource issues
   - Verify security considerations

5. **Deployment Phase**
   - Package extracted component
   - Update deployment scripts
   - Deploy to staging environment
   - Validate in production-like environment

### Quality Assurance
- **Code Review**: Conduct thorough code review
- **Testing**: Implement comprehensive test coverage
- **Documentation**: Create complete documentation
- **Performance**: Validate performance requirements
- **Security**: Conduct security review

---

## Testing Strategy

### Test Categories
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **System Tests**: Test complete system functionality
- **Performance Tests**: Validate performance requirements
- **Security Tests**: Test security characteristics

### Test Environment Setup
- **Isolated Environment**: Test in isolated environment
- **Realistic Data**: Use realistic test data
- **Edge Cases**: Test edge cases and error conditions
- **Load Testing**: Test under realistic load conditions
- **Regression Testing**: Ensure changes don't break existing functionality

### Continuous Testing
- **Automated Testing**: Implement automated test execution
- **Test Coverage**: Maintain high test coverage
- **Test Reporting**: Generate comprehensive test reports
- **Failure Analysis**: Analyze and address test failures
- **Test Maintenance**: Keep tests up to date with code changes

---

## Documentation Requirements

### Required Documentation
- **README.md**: Overview, installation, and basic usage
- **API Documentation**: Complete API reference
- **Architecture Documentation**: System design and architecture
- **Usage Examples**: Practical usage examples
- **Configuration Guide**: Configuration options and setup
- **Troubleshooting Guide**: Common issues and solutions

### Documentation Standards
- **Clear Language**: Use clear, concise language
- **Complete Coverage**: Document all public functionality
- **Up-to-Date**: Keep documentation current with code
- **Examples**: Include practical examples
- **Visual Aids**: Use diagrams and screenshots where helpful

---

## Deployment and Packaging

### Package Structure
- **Distribution Format**: Choose appropriate distribution format
- **Version Management**: Implement semantic versioning
- **Metadata**: Include complete package metadata
- **Dependencies**: Clearly specify all dependencies
- **License**: Include appropriate license information

### Deployment Strategy
- **Staging Environment**: Test in staging before production
- **Rollback Plan**: Have rollback plan ready
- **Monitoring**: Implement monitoring and alerting
- **Health Checks**: Include health check endpoints
- **Documentation**: Document deployment procedures

---

## Maintenance and Evolution

### Ongoing Maintenance
- **Bug Fixes**: Address bugs promptly
- **Security Updates**: Apply security updates quickly
- **Performance Optimization**: Monitor and optimize performance
- **Documentation Updates**: Keep documentation current
- **User Support**: Provide user support and guidance

### Evolution Planning
- **Version Strategy**: Plan version evolution strategy
- **Backward Compatibility**: Maintain backward compatibility
- **Migration Guides**: Provide migration guides for breaking changes
- **Deprecation Policy**: Implement clear deprecation policy
- **Community Engagement**: Engage with user community

---

## Best Practices

### Code Organization
- **Logical Grouping**: Group related functionality together
- **Clear Interfaces**: Design clear, intuitive interfaces
- **Minimal Coupling**: Minimize coupling between components
- **High Cohesion**: Maintain high cohesion within components
- **Consistent Style**: Follow consistent coding style

### Project Management
- **Clear Goals**: Define clear extraction goals
- **Regular Reviews**: Conduct regular progress reviews
- **Risk Management**: Identify and mitigate risks
- **Stakeholder Communication**: Keep stakeholders informed
- **Quality Focus**: Maintain focus on quality throughout process

### Technical Excellence
- **Performance**: Optimize for performance requirements
- **Scalability**: Design for scalability needs
- **Reliability**: Implement robust error handling
- **Security**: Follow security best practices
- **Maintainability**: Design for long-term maintainability 