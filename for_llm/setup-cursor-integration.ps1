# Plane-Cursor Integration Setup Script
# Run this script to configure Cursor for Plane integration

Write-Host "🚀 Plane-Cursor Integration Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check if Plane is running
Write-Host "`n1. Checking Plane deployment..." -ForegroundColor Yellow
$planeContainers = docker ps --filter "name=plane-working" --format "table {{.Names}}\t{{.Status}}"
if ($planeContainers) {
    Write-Host "✅ Plane containers are running:" -ForegroundColor Green
    Write-Host $planeContainers
} else {
    Write-Host "❌ Plane containers not found. Please start Plane first:" -ForegroundColor Red
    Write-Host "   docker-compose up -d" -ForegroundColor Cyan
    exit 1
}

# Test web interface
Write-Host "`n2. Testing Plane web interface..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:51534" -Method GET -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Plane web interface is accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Plane web interface not accessible at http://localhost:51534" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Please check if Plane is running and accessible" -ForegroundColor Yellow
    exit 1
}

# Find Cursor configuration directory
Write-Host "`n3. Locating Cursor configuration..." -ForegroundColor Yellow
$cursorConfigPaths = @(
    "$env:APPDATA\Cursor\User\mcp.json",
    "$env:LOCALAPPDATA\Cursor\User\mcp.json",
    "$env:USERPROFILE\.cursor\mcp.json"
)

$cursorConfigPath = $null
foreach ($path in $cursorConfigPaths) {
    $dir = Split-Path $path -Parent
    if (Test-Path $dir) {
        $cursorConfigPath = $path
        break
    }
}

if (-not $cursorConfigPath) {
    Write-Host "❌ Could not find Cursor configuration directory." -ForegroundColor Red
    Write-Host "   Please create the MCP configuration manually." -ForegroundColor Yellow
    Write-Host "   Expected locations:" -ForegroundColor Yellow
    foreach ($path in $cursorConfigPaths) {
        Write-Host "   - $path" -ForegroundColor Cyan
    }
} else {
    Write-Host "✅ Found Cursor configuration directory: $(Split-Path $cursorConfigPath -Parent)" -ForegroundColor Green
}

# Read the configuration template
Write-Host "`n4. Preparing MCP configuration..." -ForegroundColor Yellow
$configTemplate = Get-Content "cursor-mcp-config.json" -Raw | ConvertFrom-Json

# Update the path to use the current directory and Python server
$currentPath = (Get-Location).Path
$configTemplate.mcpServers.plane.args[0] = "$currentPath\for_llm\plane-mcp-server.py"
$configTemplate.mcpServers.plane.command = "python"
$configTemplate.mcpServers.plane.env.PLANE_MCP_PORT = "43533"

Write-Host "✅ MCP server path: $($configTemplate.mcpServers.plane.args[0])" -ForegroundColor Green
Write-Host "✅ MCP server port: 43533" -ForegroundColor Green

# Check if Cursor MCP config exists
if ($cursorConfigPath -and (Test-Path $cursorConfigPath)) {
    Write-Host "`n5. Existing MCP configuration found..." -ForegroundColor Yellow
    $existingConfig = Get-Content $cursorConfigPath -Raw | ConvertFrom-Json
    
    # Merge configurations
    if (-not $existingConfig.mcpServers) {
        $existingConfig | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue @{}
    }
    $existingConfig.mcpServers | Add-Member -NotePropertyName "plane" -NotePropertyValue $configTemplate.mcpServers.plane -Force
    
    # Backup existing config
    $backupPath = "$cursorConfigPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $cursorConfigPath $backupPath
    Write-Host "✅ Backed up existing config to: $backupPath" -ForegroundColor Green
    
    # Write updated config
    $existingConfig | ConvertTo-Json -Depth 10 | Set-Content $cursorConfigPath
    Write-Host "✅ Updated existing MCP configuration" -ForegroundColor Green
} elseif ($cursorConfigPath) {
    Write-Host "`n5. Creating new MCP configuration..." -ForegroundColor Yellow
    # Create directory if it doesn't exist
    $configDir = Split-Path $cursorConfigPath -Parent
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    
    # Write new config
    $configTemplate | ConvertTo-Json -Depth 10 | Set-Content $cursorConfigPath
    Write-Host "✅ Created new MCP configuration: $cursorConfigPath" -ForegroundColor Green
}

Write-Host "`n6. Next steps:" -ForegroundColor Yellow
Write-Host "   1. Open Plane in your browser: http://localhost:8080" -ForegroundColor Cyan
Write-Host "   2. Create an account and workspace if needed" -ForegroundColor Cyan
Write-Host "   3. Go to Settings → API → Create API Token" -ForegroundColor Cyan
Write-Host "   4. Copy the API token" -ForegroundColor Cyan
Write-Host "   5. Edit the MCP configuration to add your API key:" -ForegroundColor Cyan
if ($cursorConfigPath) {
    Write-Host "      $cursorConfigPath" -ForegroundColor White
}
Write-Host "   6. Replace 'your_plane_api_key_here' with your actual API key" -ForegroundColor Cyan
Write-Host "   7. Restart Cursor completely" -ForegroundColor Cyan
Write-Host "   8. Test the integration by asking: 'List all workspaces in Plane'" -ForegroundColor Cyan

Write-Host "`n🎉 Setup complete! Ready for API key configuration." -ForegroundColor Green

# Test the MCP server
Write-Host "`n7. Testing MCP server..." -ForegroundColor Yellow
try {
    $env:PLANE_API_URL = "http://localhost:51534"
    $env:PLANE_API_KEY = "test"
    $env:PLANE_MCP_PORT = "43533"
    python "for_llm/plane-mcp-server.py" --help 2>$null
    Write-Host "✅ MCP server is ready" -ForegroundColor Green
} catch {
    Write-Host "⚠️  MCP server test skipped (normal - needs API key)" -ForegroundColor Yellow
}

Write-Host "`nFor troubleshooting, see: SETUP_INSTRUCTIONS.md" -ForegroundColor Cyan 