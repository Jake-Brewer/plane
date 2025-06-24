# LLM Documentation Management Guide
# Last Updated: 2025-01-27T00:00:00Z

## Overview

This guide provides comprehensive instructions for managing, updating, and maintaining LLM documentation files (_llm*.md files) that provide guidance to AI assistants working on the project.

## Documentation Structure

### Protected Files (NEVER DELETE)
- `_llm_primer.md` - Core behavioral standards (root level)
- `_llm_project_primer.md` - Project-specific context (root level)
- All files in `for_llm/` directory - Specialized guidance

### Specialized Guidance Files
- `for_llm/_llm_agent_registry.md` - Agent coordination and registration
- `for_llm/_llm_model_selection_guide.md` - LLM model selection and optimization
- `for_llm/_llm_linear_project_management.md` - Linear integration
- `for_llm/_llm_extraction_primer.md` - Component extraction
- `for_llm/_llm_multi-agent_primer.md` - Multi-agent collaboration
- `for_llm/_llm_port_management.md` - Port configuration
- `for_llm/_llm_cursor_mcp_management.md` - MCP server management
- `for_llm/_llm_documentation_management.md` - This file
- `for_llm/LINEAR_API_CREDENTIALS.md` - API authentication

## File Management Standards

### Naming Conventions
- **Core Files**: `_llm_primer.md`, `_llm_project_primer.md` (root level)
- **Specialized Files**: `_llm_<domain>_<purpose>.md` (in for_llm/)
- **Reference Files**: `<TOPIC>_<TYPE>.md` (in for_llm/)
- **Todo Files**: `for_llm_todo_<agent-name>.md`

### File Headers
All LLM guidance files must include:
```markdown
# File Title
# Last Updated: YYYY-MM-DDTHH:MM:SSZ

## Overview
Brief description of the file's purpose and scope.
```

### Update Timestamps
**CRITICAL**: Always update the "Last Updated" timestamp when modifying files:
```markdown
# Last Updated: 2025-01-27T00:00:00Z
```

## Adding New Guidance Files

### 1. Determine File Type and Location

#### Core Guidance (Root Level)
Only for fundamental behavioral standards that apply to ALL interactions:
- `_llm_primer.md` - Universal behavioral standards
- `_llm_project_primer.md` - Project-specific context

#### Specialized Guidance (for_llm/ Directory)
For domain-specific or task-specific guidance:
- Port management, MCP servers, Linear integration, etc.
- Named as `_llm_<domain>_<purpose>.md`

#### Reference Files (for_llm/ Directory)
For configuration templates, credentials, or reference data:
- API credentials, configuration examples, etc.
- Named as `<TOPIC>_<TYPE>.md`

### 2. Create the New File
```markdown
# [File Title]
# Last Updated: [Current ISO timestamp]

## Overview
[Brief description of purpose and scope]

## [Content sections...]

---

## Quick Reference
[Key commands/procedures for easy access]

**Remember**: [Key reminders or warnings]
```

### 3. Update Navigation References

#### Update _llm_primer.md Navigation Map
Add new specialized guidance to the navigation map:
```markdown
### Navigation Map
- **New Domain** → `for_llm/_llm_new_domain.md`
```

#### Update Task-Specific Navigation Guide
Add trigger conditions for when to access the new guidance:
```markdown
#### 🔧 New Domain Management
**Access:** `for_llm/_llm_new_domain.md`
**Triggers:**
- Specific condition 1
- Specific condition 2
- Specific condition 3
```

### 4. Update FOLDER_GUIDE.md
Add the new file to the appropriate FOLDER_GUIDE.md:
```markdown
- `_llm_new_domain.md` - Brief description of purpose
```

## Updating Existing Files

### 1. Standard Update Procedure
1. **Read current file** to understand existing content
2. **Make necessary changes** while preserving structure
3. **Update timestamp** in file header
4. **Test references** to ensure links still work
5. **Commit changes** with descriptive message

### 2. Breaking Changes Procedure
For changes that affect other files or workflows:

1. **Backup current state**
   ```powershell
   git add -A
   git commit -m "Backup before LLM documentation changes"
   ```

2. **Update dependent files** simultaneously
3. **Update navigation references** if file names change
4. **Test complete workflow** to ensure nothing is broken
5. **Commit all changes together**

### 3. Timestamp Management
Always update timestamps when making ANY changes:
```markdown
# Last Updated: 2025-01-27T14:30:00Z  # Use current UTC time
```

## Content Standards

### Writing Style
- **Clear and Direct**: Use simple, actionable language
- **Structured**: Use consistent heading hierarchy
- **Practical**: Include specific commands and examples
- **Complete**: Provide all necessary context

### Required Sections
1. **Overview** - Purpose and scope
2. **Main Content** - Organized by logical sections
3. **Quick Reference** - Key commands/procedures
4. **Remember Statement** - Critical warnings or reminders

### Code Examples
Include practical, working examples:
```powershell
# Windows PowerShell example
Get-Random -Minimum 10000 -Maximum 65535
```

```bash
# Linux/Mac example
netstat -tuln | grep :PORT_NUMBER
```

### Cross-References
Link to related guidance files:
```markdown
See also: `for_llm/_llm_related_topic.md` for additional details.
```

## Version Control Integration

### Commit Message Standards
```bash
# For new files
git commit -m "Add LLM guidance for [domain]: [brief description]

- Created for_llm/_llm_[domain].md with comprehensive guidance
- Updated _llm_primer.md navigation references
- Added to FOLDER_GUIDE.md documentation"

# For updates
git commit -m "Update LLM guidance: [specific change]

- Updated for_llm/_llm_[domain].md with [changes]
- Refreshed timestamp and validated references
- [Any other related changes]"
```

### Backup Procedures
```powershell
# Create backup of all LLM files before major changes
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = ".\backups\llm-docs-$timestamp"
New-Item -ItemType Directory -Path $backupDir -Force

# Backup root level LLM files
Copy-Item "_llm*.md" $backupDir

# Backup for_llm directory
Copy-Item "for_llm" $backupDir -Recurse

Write-Host "LLM documentation backed up to: $backupDir"
```

## Quality Assurance

### Pre-Commit Checklist
- [ ] Timestamp updated in file header
- [ ] Navigation references updated if needed
- [ ] Cross-references validated
- [ ] Code examples tested
- [ ] FOLDER_GUIDE.md updated
- [ ] No protected files deleted or moved
- [ ] Commit message follows standards

### Validation Commands
```powershell
# Check for missing timestamps
Get-ChildItem -Path "." -Filter "_llm*.md" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Head 5
    if ($content -notmatch "Last Updated:") {
        Write-Warning "Missing timestamp: $($_.FullName)"
    }
}

# Validate file references
Get-ChildItem -Path "for_llm" -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match "`for_llm/([^`]+)`") {
        $references = $Matches[1]
        # Check if referenced files exist
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Broken References
**Symptoms**: References to non-existent files
**Solutions**:
- Check file paths are correct
- Update references when files are renamed
- Use relative paths consistently

#### 2. Outdated Information
**Symptoms**: Instructions don't match current system
**Solutions**:
- Regular review and validation
- Update timestamps when content changes
- Test procedures before documenting

#### 3. Inconsistent Structure
**Symptoms**: Files don't follow standard format
**Solutions**:
- Use template structure for new files
- Standardize existing files during updates
- Maintain consistent heading hierarchy

### Recovery Procedures
```powershell
# Restore from backup
$backupDir = ".\backups\llm-docs-TIMESTAMP"
Copy-Item "$backupDir\_llm*.md" "." -Force
Copy-Item "$backupDir\for_llm\*" "for_llm\" -Force -Recurse

# Restore from git
git checkout HEAD -- _llm*.md for_llm/
```

## Advanced Management

### Automated Maintenance
```powershell
# Script to update all timestamps
$files = Get-ChildItem -Path "." -Filter "_llm*.md" -Recurse
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

foreach ($file in $files) {
    $content = Get-Content $file.FullName
    $updated = $content -replace "# Last Updated: .*", "# Last Updated: $timestamp"
    Set-Content $file.FullName $updated
}
```

### Documentation Analytics
```powershell
# Analyze documentation coverage
$domains = @("port", "mcp", "linear", "extraction", "multi-agent")
foreach ($domain in $domains) {
    $file = "for_llm\_llm_*$domain*.md"
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "$domain : $size bytes"
    } else {
        Write-Warning "$domain : No documentation found"
    }
}
```

---

## Quick Reference

### Create New LLM Guidance File
1. Determine file type and location
2. Create file with standard structure
3. Update _llm_primer.md navigation
4. Update FOLDER_GUIDE.md
5. Test and commit changes

### Update Existing File
1. Make content changes
2. Update timestamp in header
3. Validate cross-references
4. Commit with descriptive message

### Backup LLM Documentation
```powershell
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = ".\backups\llm-docs-$timestamp"
New-Item -ItemType Directory -Path $backupDir -Force
Copy-Item "_llm*.md" $backupDir
Copy-Item "for_llm" $backupDir -Recurse
```

**Remember**: LLM documentation files are critical project infrastructure. Always backup before major changes, maintain consistent structure, and update timestamps when making any modifications. 