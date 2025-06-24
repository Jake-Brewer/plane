#!/bin/bash
# Plane Multi-Agent Configuration Script
# Sets up role-based access for LLM agents
# Usage: ./configure-agents.sh

set -e

CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"
CONFIG_DIR="Z:/plane-data/agent-config"

echo "🤖 Configuring multi-agent access system..."
mkdir -p "$CONFIG_DIR"

# Agent configuration template
cat > "$CONFIG_DIR/agent-roles.json" << 'EOF'
{
  "agent_roles": {
    "developer": {
      "description": "Full development access to assigned projects",
      "permissions": ["read", "write", "comment", "assign"],
      "rate_limit": "300/minute",
      "timeout_hours": 4,
      "projects": "assigned_only"
    },
    "reviewer": {
      "description": "Review and comment access across projects", 
      "permissions": ["read", "comment", "review"],
      "rate_limit": "150/minute", 
      "timeout_hours": 2,
      "projects": "all"
    },
    "reporter": {
      "description": "Read-only access for reporting and analytics",
      "permissions": ["read"],
      "rate_limit": "100/minute",
      "timeout_hours": 1,
      "projects": "all"
    },
    "admin": {
      "description": "Administrative access for system management",
      "permissions": ["read", "write", "comment", "assign", "admin"],
      "rate_limit": "500/minute",
      "timeout_hours": 8,
      "projects": "all"
    }
  }
}
EOF

# Agent timeout monitoring script
cat > "$CONFIG_DIR/monitor-agent-timeouts.sh" << 'EOF'
#!/bin/bash
# Monitor agent work assignments and reset stalled items
# Run every 30 minutes via cron

TIMEOUT_HOURS=${1:-4}  # Default 4 hour timeout
CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"

echo "Checking for stalled agent assignments (timeout: ${TIMEOUT_HOURS}h)..."

# SQL to find stalled assignments (issues assigned but no recent activity)
STALLED_QUERY="
SELECT 
    i.id,
    i.name,
    i.assignee_id,
    u.email as assignee_email,
    i.updated_at,
    EXTRACT(EPOCH FROM (NOW() - i.updated_at))/3600 as hours_since_update
FROM plane_issue i
LEFT JOIN plane_user u ON i.assignee_id = u.id
WHERE i.assignee_id IS NOT NULL
  AND i.state_id IN (SELECT id FROM plane_state WHERE name IN ('In Progress', 'Todo'))
  AND i.updated_at < NOW() - INTERVAL '${TIMEOUT_HOURS} hours'
  AND NOT EXISTS (
    SELECT 1 FROM plane_issuecomment ic 
    WHERE ic.issue_id = i.id 
    AND ic.created_at > NOW() - INTERVAL '${TIMEOUT_HOURS} hours'
  );
"

# Execute query and log results
docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "$STALLED_QUERY" > /tmp/stalled_assignments.txt

if [ -s /tmp/stalled_assignments.txt ]; then
    echo "⚠️ Found stalled assignments:"
    cat /tmp/stalled_assignments.txt
    
    # TODO: Implement auto-reassignment logic here
    # For now, just log the findings
    echo "$(date): Stalled assignments detected" >> "Z:/plane-data/logs/agent-timeouts.log"
    cp /tmp/stalled_assignments.txt "Z:/plane-data/logs/stalled_$(date +%Y%m%d_%H%M%S).txt"
else
    echo "✅ No stalled assignments found"
fi

rm -f /tmp/stalled_assignments.txt
EOF

chmod +x "$CONFIG_DIR/monitor-agent-timeouts.sh"

# Agent activity monitoring script
cat > "$CONFIG_DIR/monitor-agent-activity.sh" << 'EOF'
#!/bin/bash
# Monitor agent API activity and generate reports
# Usage: ./monitor-agent-activity.sh [hours_back]

HOURS_BACK=${1:-24}  # Default last 24 hours
CONTAINER_NAME="plane-db"
DB_NAME="plane"
DB_USER="plane_admin"
REPORT_DIR="Z:/plane-data/agent-reports"

mkdir -p "$REPORT_DIR"
REPORT_FILE="$REPORT_DIR/agent_activity_$(date +%Y%m%d_%H%M%S).txt"

echo "Agent Activity Report - Last ${HOURS_BACK} hours" > "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo "=============================================" >> "$REPORT_FILE"

# Query agent activity (assuming API tokens are used for agents)
ACTIVITY_QUERY="
SELECT 
    at.label as agent_name,
    COUNT(*) as api_calls,
    MAX(at.last_used) as last_activity,
    u.email as owner_email
FROM plane_apitoken at
LEFT JOIN plane_user u ON at.user_id = u.id
WHERE at.last_used > NOW() - INTERVAL '${HOURS_BACK} hours'
  AND at.label LIKE '%agent%' OR at.label LIKE '%bot%'
GROUP BY at.id, at.label, u.email
ORDER BY api_calls DESC;
"

echo "Active Agents (Last ${HOURS_BACK} hours):" >> "$REPORT_FILE"
echo "----------------------------------------" >> "$REPORT_FILE"
docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c "$ACTIVITY_QUERY" >> "$REPORT_FILE" 2>/dev/null || echo "No agent activity data available" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "Report saved to: $REPORT_FILE"
EOF

chmod +x "$CONFIG_DIR/monitor-agent-activity.sh"

# Create agent setup instructions
cat > "$CONFIG_DIR/AGENT_SETUP.md" << 'EOF'
# Multi-Agent Setup Instructions

## Creating Agent API Tokens

1. Access Plane admin interface: http://localhost
2. Navigate to Settings > API Tokens
3. Create new token:
   - **Name**: agent-[role]-[identifier] (e.g., agent-developer-001)
   - **Type**: Service Token (300 req/min rate limit)
   - **Scope**: Project-specific or workspace-wide based on role
   - **Expiration**: 90 days (recommended)

## Agent Role Configuration

Refer to `agent-roles.json` for role definitions:
- **developer**: Full access to assigned projects
- **reviewer**: Review access across all projects  
- **reporter**: Read-only access for analytics
- **admin**: Full administrative access

## Monitoring Commands

```bash
# Check for stalled assignments
./monitor-agent-timeouts.sh

# Generate activity report
./monitor-agent-activity.sh 24

# Monitor real-time API activity
docker-compose logs api | grep "API_TOKEN"
```

## Timeout Management

Agents that don't update their assigned work within the timeout period will be flagged:
- **Developer agents**: 4 hour timeout
- **Reviewer agents**: 2 hour timeout  
- **Reporter agents**: 1 hour timeout
- **Admin agents**: 8 hour timeout

## Best Practices

1. Use descriptive agent names (agent-developer-frontend-001)
2. Set appropriate token expiration dates
3. Monitor agent activity regularly
4. Implement work reassignment for stalled items
5. Rotate tokens quarterly for security
EOF

echo "✅ Multi-agent configuration completed!"
echo ""
echo "📁 Configuration files created:"
echo "   - $CONFIG_DIR/agent-roles.json"
echo "   - $CONFIG_DIR/monitor-agent-timeouts.sh"  
echo "   - $CONFIG_DIR/monitor-agent-activity.sh"
echo "   - $CONFIG_DIR/AGENT_SETUP.md"
echo ""
echo "🔧 Next steps:"
echo "1. Review agent roles in agent-roles.json"
echo "2. Set up cron job for timeout monitoring:"
echo "   */30 * * * * $CONFIG_DIR/monitor-agent-timeouts.sh"
echo "3. Create API tokens following AGENT_SETUP.md instructions" 