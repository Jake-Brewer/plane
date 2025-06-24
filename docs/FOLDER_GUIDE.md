# Documentation Directory Guide
# Last Updated: 2025-01-27T00:53:00Z

## Purpose

This directory contains project documentation, research materials, and analysis documents for the Plane project. It serves as the central repository for human-readable documentation that supports development and operational activities.

## Scope

### In-Scope
- Project documentation and guides
- Research findings and analysis
- Technical specifications and architecture documents
- User guides and operational procedures
- Analysis and reference materials for development workflows
- Security assessments and operational analysis

### Out-of-Scope
- Direct LLM operational guidance (see `for_llm/` directory)
- Source code and implementation files
- Configuration files and deployment scripts
- Temporary files and build artifacts

## Directory Structure

```
docs/
├── FOLDER_GUIDE.md (This file)
├── local_deployment_security_assessment.md # Security assessment for local deployment
├── revised_security_assessment_prompt.md # Improved security assessment prompt
├── research/           # Research findings and analysis
│   └── llm/           # LLM-related research and evaluations
└── working_with_llm/   # LLM analysis and reference materials
```

## Files in This Directory

### Security and Operational Analysis
- **`local_deployment_security_assessment.md`** (12KB, 285 lines)
  - Comprehensive security assessment for local Plane deployment
  - Multi-agent LLM access control analysis
  - Data integrity and backup strategy recommendations
  - Docker container security evaluation
  - MCP integration security requirements

- **`revised_security_assessment_prompt.md`** (4KB, 95 lines)
  - Improved security assessment prompt template
  - Context-specific for local deployment scenarios
  - Multi-agent workflow considerations
  - Priority-focused security concerns

## Subdirectory Details

### research/
Contains research findings, analysis, and evaluation materials.

**Current Contents:**
- `llm/` - LLM provider evaluations, performance analysis, and recommendations (11 files)
  - `preparation.md` - LLM setup and preparation guidelines (16KB, 350 lines)
  - `ratings.md` - Comparative analysis of LLM providers (6KB, 104 lines)
  - `strengths-and-weaknesses.md` - Detailed evaluation of LLM capabilities (9.5KB, 224 lines)
  - `project_analysis_selector.md` - Project analysis selection guidance (18KB, 459 lines)
  - `project_analysis_prompt.md` - Project analysis prompting guide (11KB)
  - `model_style_guide.md` - Model style and usage guidelines (23KB, 368 lines)
  - `model_selection_prompt.md` - Model selection prompting strategies (7KB, 150 lines)
  - `cheapest_model_selector.md` - Cost-effective model selection guide (10KB, 284 lines)
  - `model_selector.py` - Python model selection utility (25KB, modified)
  - `model_selection_results.json` - Model selection results data (new)
  - `sample_config.json` - Sample configuration file (new)

### working_with_llm/
Contains analysis and reference materials for LLM agent workflows.

**Purpose:** Human-readable analysis and reference materials complementing the direct LLM guidance in `for_llm/` directory.

**See:** `working_with_llm/FOLDER_GUIDE.md` for detailed information.

## Content Guidelines

### Documentation Standards
- **Clear Structure**: Organized hierarchy with logical grouping
- **Comprehensive Coverage**: Complete documentation of relevant topics
- **Searchable**: Well-structured for easy navigation and searching
- **Maintained**: Regular updates to keep content current
- **Cross-Referenced**: Links to related materials and resources

### Security Documentation Standards
- **Risk-Based Analysis**: Clear risk assessment matrices
- **Actionable Recommendations**: Specific implementation guidance
- **Priority Classification**: Clear priority levels for security concerns
- **Implementation Timeline**: Phased implementation approaches

### File Naming Conventions
- **Descriptive Names**: Clear indication of content and purpose
- **Consistent Format**: Follow established naming patterns
- **Version Indicators**: Include dates or versions where appropriate
- **Category Prefixes**: Use prefixes to indicate document type

## Maintenance Responsibilities

### Content Management
- **Regular Reviews**: Periodic review for accuracy and relevance
- **Version Control**: Track changes and maintain history
- **Quality Assurance**: Ensure documentation meets standards
- **Cross-Reference Validation**: Verify links and references remain valid

### Security Documentation Maintenance
- **Regular Security Reviews**: Update assessments based on new threats
- **Implementation Tracking**: Monitor implementation of security recommendations
- **Validation Testing**: Verify security measures are effective
- **Compliance Updates**: Keep security standards current

### Organization
- **Logical Structure**: Maintain clear directory organization
- **Consistent Standards**: Apply consistent formatting and structure
- **Archive Management**: Archive outdated content appropriately
- **Index Maintenance**: Keep directory guides current

## Integration Points

### Related Directories
- **`for_llm/`**: Direct LLM operational guidance and instructions
- **`packages/`**: Source code packages with their own documentation
- **Root Documentation**: Main project documentation files (README.md, etc.)

### Cross-References
- Documentation may reference implementation details in source code
- Research findings may inform LLM guidance and operational procedures
- Analysis materials may reference external resources and documentation
- Security assessments reference deployment configurations and source code

---

**Note**: This directory focuses on human-readable documentation and analysis. For direct LLM operational guidance, see the `for_llm/` directory. For core project information, see the root-level documentation files. 