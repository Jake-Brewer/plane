# Working with LLM - Analysis and Reference Materials
# Last Updated: 2025-01-27T00:00:00Z

## Purpose

This directory contains analysis and reference materials for working with LLM agents in the Plane project. Unlike the `for_llm/` directory which contains direct LLM guidance, this directory holds human-readable analysis, research, and reference materials.

## Scope

### In-Scope
- LLM performance analysis and benchmarking
- Integration testing results and reports
- Historical decision records and rationale
- Research findings and recommendations
- Case studies and lessons learned
- Reference implementations and examples

### Out-of-Scope
- Direct LLM guidance (see `for_llm/` directory)
- Project-specific operational instructions (see `_llm_project_primer.md`)
- Core behavioral standards (see `_llm_primer.md`)
- Real-time working notes (see `for_llm/llm_owned_notes/`)

## Directory Structure

```
docs/working_with_llm/
├── FOLDER_GUIDE.md (This file)
├── analysis/           # Analysis reports and findings
├── benchmarks/         # Performance benchmarking results
├── case_studies/       # Detailed case studies and examples
├── decisions/          # Architectural decision records
├── integration_tests/  # Integration testing results
├── research/           # Research findings and recommendations
└── templates/          # Reusable templates and examples
```

## Content Guidelines

### Documentation Standards
- **Human-Readable**: Written for human analysis and review
- **Comprehensive**: Detailed analysis with supporting data
- **Searchable**: Well-structured for easy searching and reference
- **Version Controlled**: Track changes and evolution over time
- **Cross-Referenced**: Link to related materials and decisions

### File Naming Conventions
- **Dates**: Use ISO 8601 format (YYYY-MM-DD) for time-based content
- **Descriptive**: Clear, descriptive names indicating content type
- **Versioned**: Include version numbers for evolving documents
- **Categorized**: Use subdirectories for logical organization

## Integration with LLM Guidance

### Relationship to for_llm/ Directory
- **Complementary**: Provides background and analysis for LLM guidance
- **Reference**: LLM guidance files may reference materials here
- **Historical**: Maintains historical context for current guidance
- **Evidence-Based**: Provides evidence backing LLM guidance decisions

### Usage Patterns
- **Research Phase**: Analyze and document findings here
- **Implementation Phase**: Reference analysis when creating LLM guidance
- **Maintenance Phase**: Update analysis based on operational experience
- **Review Phase**: Periodic review and validation of guidance effectiveness

## Maintenance Responsibilities

### Content Lifecycle
- **Creation**: Document new analysis and findings as they occur
- **Updates**: Keep content current with project evolution
- **Archival**: Archive outdated content with clear historical context
- **Cleanup**: Regular cleanup of redundant or obsolete materials

### Quality Assurance
- **Accuracy**: Ensure all analysis is factually accurate
- **Completeness**: Document complete analysis including limitations
- **Objectivity**: Maintain objective, evidence-based analysis
- **Reproducibility**: Provide sufficient detail for reproduction

## Current Contents

### Existing Materials
- **LLM Research**: Performance evaluations and recommendations (docs/research/llm/)
- **Preparation Guides**: Setup and preparation documentation
- **Ratings Analysis**: Comparative analysis of different LLM providers

### Planned Materials
- **Integration Benchmarks**: Linear API integration performance testing
- **Case Studies**: Successful LLM-assisted development workflows
- **Decision Records**: Key architectural and technical decisions
- **Best Practices**: Documented best practices from operational experience

---

**Note**: This directory contains human-readable analysis and reference materials. For direct LLM operational guidance, see the `for_llm/` directory. For core behavioral standards, see `_llm_primer.md` in the project root. 