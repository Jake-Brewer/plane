# Linear Project Management - Comprehensive Guide
# Last Updated: 2025-01-27T00:00:00Z

**PREREQUISITE**: Read `_llm_primer.md` first for core behavioral standards

## Overview

This guide provides comprehensive instructions for using Linear to manage projects, issues, and workflows in the docker-command-center ecosystem. Linear serves as the central project management hub with OAuth integration for seamless operation.

### Authentication Setup
**Reference**: `for_llm/LINEAR_API_CREDENTIALS.md` for detailed authentication instructions

---

## Issue Management

### Creating Issues
1. **Title**: Clear, descriptive titles that indicate the work scope
2. **Description**: Detailed description with acceptance criteria
3. **Priority**: Set appropriate priority (Urgent, High, Medium, Low)
4. **Labels**: Apply relevant labels for categorization
5. **Assignee**: Assign to appropriate team member
6. **Project**: Link to relevant project
7. **Dependencies**: Set up issue dependencies if applicable

### Issue Structure Template
```markdown
## Objective
Clear statement of what needs to be accomplished

## Requirements
- Specific requirement 1
- Specific requirement 2
- Specific requirement 3

## Acceptance Criteria
- [ ] Criteria 1 that must be met
- [ ] Criteria 2 that must be met
- [ ] Criteria 3 that must be met

## Dependencies
- Issue #XXX must be completed first
- External dependency on Y

## Deliverables
- Specific deliverable 1
- Specific deliverable 2
```

### Issue Status Management
- **Backlog**: Issue is identified but not yet started
- **Todo**: Issue is ready to be worked on
- **In Progress**: Work has begun on the issue
- **In Review**: Work is complete and under review
- **Done**: Issue is complete and verified
- **Canceled**: Issue is no longer needed
- **Duplicate**: Issue duplicates another issue

---

## Project Organization

### Project Structure
1. **Project Overview**: Clear description of project goals
2. **Milestones**: Key deliverables and deadlines
3. **Roadmap**: High-level timeline and phases
4. **Team Members**: Roles and responsibilities
5. **Success Metrics**: How success will be measured

### Project Types
- **Feature Projects**: New functionality development
- **Maintenance Projects**: Ongoing system maintenance
- **Research Projects**: Investigation and analysis
- **Infrastructure Projects**: System improvements
- **Bug Fix Projects**: Issue resolution

### Project Lifecycle
1. **Planning**: Define scope, goals, and requirements
2. **Execution**: Implement planned work
3. **Monitoring**: Track progress and adjust as needed
4. **Closure**: Complete deliverables and document outcomes

---

## Dependency Management

### Dependency Types
- **Blocking**: Issue cannot start until dependency is complete
- **Related**: Issues are connected but not blocking
- **Duplicate**: Multiple issues for the same work
- **Subtask**: Issue is part of a larger issue

### Setting Up Dependencies
1. **Identify Dependencies**: Determine what work must be done first
2. **Create Dependency Links**: Use Linear's dependency features
3. **Validate Order**: Ensure logical work sequence
4. **Monitor Progress**: Track dependency completion
5. **Adjust as Needed**: Modify dependencies when requirements change

### Dependency Best Practices
- **Clear Relationships**: Make dependency reasons explicit
- **Minimal Dependencies**: Only create necessary dependencies
- **Regular Review**: Check dependencies for continued relevance
- **Communication**: Notify stakeholders of dependency changes

---

## Workflow Management

### Standard Workflow
1. **Issue Creation**: Create detailed issue with requirements
2. **Planning**: Break down work and estimate effort
3. **Assignment**: Assign to appropriate team member
4. **Execution**: Complete the work as specified
5. **Review**: Validate work meets requirements
6. **Closure**: Mark issue as complete

### Workflow Automation
- **Status Transitions**: Automatic status updates based on actions
- **Notifications**: Alert stakeholders of important changes
- **Integration**: Connect with GitHub, Slack, and other tools
- **Reporting**: Generate progress reports automatically

### Custom Workflows
- **Development Workflow**: Code → Review → Test → Deploy
- **Design Workflow**: Concept → Design → Review → Implement
- **Research Workflow**: Question → Research → Analysis → Report

---

## Progress Tracking

### Tracking Methods
- **Issue Status**: Monitor individual issue progress
- **Project Progress**: Track overall project completion
- **Milestone Progress**: Monitor key deliverable completion
- **Team Progress**: Track individual and team productivity

### Metrics and KPIs
- **Velocity**: Issues completed per time period
- **Cycle Time**: Time from start to completion
- **Lead Time**: Time from creation to completion
- **Quality**: Defect rates and rework frequency

### Reporting
- **Daily Standups**: Brief progress updates
- **Weekly Reports**: Detailed progress summaries
- **Monthly Reviews**: Comprehensive project assessment
- **Quarterly Planning**: Strategic planning and adjustment

---

## Integration with Development

### GitHub Integration
- **Issue Linking**: Link Linear issues to GitHub PRs
- **Automatic Updates**: Status updates from GitHub actions
- **Code References**: Reference issues in commit messages
- **Branch Naming**: Use issue numbers in branch names

### Documentation Integration
- **Issue Documentation**: Link issues to relevant docs
- **Decision Records**: Document architectural decisions
- **Process Documentation**: Maintain workflow documentation
- **Knowledge Base**: Build searchable knowledge repository

### Cross-Reference Patterns
- **Linear → GitHub**: `JAK-XXX: Description`
- **GitHub → Linear**: Reference issue numbers in commits
- **Documentation → Linear**: Link to relevant issues
- **Code → Linear**: Reference issues in code comments

---

## Team Collaboration

### Communication Patterns
- **Issue Comments**: Discuss work directly on issues
- **Status Updates**: Regular progress communication
- **Blockers**: Immediate notification of impediments
- **Decisions**: Document important decisions on issues

### Review Processes
- **Peer Review**: Team member reviews work
- **Stakeholder Review**: Customer/user review
- **Technical Review**: Architecture and code review
- **Process Review**: Workflow and procedure review

### Knowledge Sharing
- **Documentation**: Maintain comprehensive documentation
- **Training**: Share knowledge across team members
- **Best Practices**: Document and share effective approaches
- **Lessons Learned**: Capture and share insights

---

## Advanced Features

### Linear API Usage
- **Automation**: Automate routine tasks using Linear API
- **Custom Integrations**: Build custom tools and integrations
- **Data Export**: Extract data for analysis and reporting
- **Bulk Operations**: Perform operations on multiple issues

### Reporting and Analytics
- **Built-in Reports**: Use Linear's reporting features
- **Custom Dashboards**: Create project-specific dashboards
- **Data Analysis**: Analyze team and project performance
- **Trend Analysis**: Identify patterns and trends over time

---

## Best Practices

### Issue Management Best Practices
- **Clear Titles**: Write descriptive, searchable titles
- **Detailed Descriptions**: Include context and requirements
- **Proper Labeling**: Use consistent labeling scheme
- **Regular Updates**: Keep issue status current
- **Documentation Links**: Reference relevant documentation

### Project Management Best Practices
- **Clear Scope**: Define project boundaries clearly
- **Regular Reviews**: Conduct periodic project reviews
- **Risk Management**: Identify and mitigate project risks
- **Stakeholder Communication**: Keep stakeholders informed
- **Documentation**: Maintain comprehensive project documentation

### Team Collaboration Best Practices
- **Communication**: Use clear, concise communication
- **Transparency**: Share information openly with team
- **Feedback**: Provide constructive feedback regularly
- **Knowledge Sharing**: Document and share learnings
- **Continuous Improvement**: Regularly review and improve processes 