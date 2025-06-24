# MCP Configuration Backup Script
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$mcpPath = "$env:APPDATA\Cursor\User\mcp.json"
$backupPath = ".\backups\mcp-configs\mcp-backup-$timestamp.json"

if (Test-Path $mcpPath) {
    Copy-Item $mcpPath $backupPath
    Write-Host "MCP configuration backed up to: $backupPath"
} else {
    Write-Host "No existing MCP configuration found at: $mcpPath"
    Write-Host "This is normal for first-time setup"
}

# Also create a backup of our configuration template
$templatePath = ".\for_llm\cursor-mcp-config.json"
$templateBackupPath = ".\backups\mcp-configs\cursor-mcp-config-$timestamp.json"

if (Test-Path $templatePath) {
    Copy-Item $templatePath $templateBackupPath
    Write-Host "Template configuration backed up to: $templateBackupPath"
}

Write-Host "Backup complete!" 