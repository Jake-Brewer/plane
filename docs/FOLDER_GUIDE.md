# Documentation Directory Guide
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains project documentation, research materials, and analysis documents for the Plane project. It serves as the central repository for human-readable documentation that supports development and operational activities.

## Scope

### In-Scope
- Project documentation and guides
- Research findings and analysis
- Technical specifications and architecture documents
- User guides and operational procedures
- Analysis and reference materials for development workflows

### Out-of-Scope
- Direct LLM operational guidance (see `for_llm/` directory)
- Source code and implementation files
- Configuration files and deployment scripts
- Temporary files and build artifacts

## Directory Structure

```
docs/
├── FOLDER_GUIDE.md (This file)
├── research/           # Research findings and analysis
│   └── llm/           # LLM-related research and evaluations
└── working_with_llm/   # LLM analysis and reference materials
```

## Subdirectory Details

### research/
Contains research findings, analysis, and evaluation materials.

**Current Contents:**
- `llm/` - LLM provider evaluations, performance analysis, and recommendations (9 files)
  - `preparation.md` - LLM setup and preparation guidelines (16KB, 350 lines)
  - `ratings.md` - Comparative analysis of LLM providers (6KB, 104 lines)
  - `strengths-and-weaknesses.md` - Detailed evaluation of LLM capabilities (9.5KB, 224 lines)
  - `project_analysis_selector.md` - Project analysis selection guidance (18KB, 459 lines)
  - `project_analysis_prompt.md` - Project analysis prompting guide (11KB)
  - `model_style_guide.md` - Model style and usage guidelines (23KB, 368 lines)
  - `model_selection_prompt.md` - Model selection prompting strategies (7KB, 150 lines)
  - `cheapest_model_selector.md` - Cost-effective model selection guide (10KB, 284 lines)
  - `model_selector.py` - Python model selection utility (25KB)

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

---

**Note**: This directory focuses on human-readable documentation and analysis. For direct LLM operational guidance, see the `for_llm/` directory. For core project information, see the root-level documentation files. 