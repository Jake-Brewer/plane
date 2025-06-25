# Simple Plane MCP Server Setup Script
Write-Host "Plane MCP Server Setup"
Write-Host "======================"

# Step 1: Check if Plane is running
Write-Host ""
Write-Host "Step 1: Checking Plane containers..."
$containers = docker ps | Select-String "plane-working"
if ($containers) {
    Write-Host "✅ Plane containers are running"
} else {
    Write-Host "❌ No Plane containers found. Please start Plane first with: docker-compose up -d"
    exit 1
}

# Step 2: Set environment variables
Write-Host ""
Write-Host "Step 2: Setting environment variables..."
$env:PLANE_API_URL = "http://localhost:51534"
$env:PLANE_MCP_PORT = "43533"
Write-Host "✅ Set PLANE_API_URL = http://localhost:51534"
Write-Host "✅ Set PLANE_MCP_PORT = 43533"

# Step 3: Check Python dependencies
Write-Host ""
Write-Host "Step 3: Checking Python dependencies..."
$packages = @("fastapi", "httpx", "prometheus_client", "starlette", "uvicorn")
$missing = @()

foreach ($package in $packages) {
    $result = pip show $package 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $package is installed"
    } else {
        $missing += $package
        Write-Host "❌ $package is missing"
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Installing missing packages..."
    pip install ($missing -join " ")
    Write-Host "✅ Python dependencies installed"
}

# Step 4: API Key setup
Write-Host ""
Write-Host "Step 4: API Key Setup"
Write-Host "You need to create a Plane API token:"
Write-Host "1. Open browser to: http://localhost:51534"
Write-Host "2. Log in to your Plane account"
Write-Host "3. Go to Settings → API Tokens"
Write-Host "4. Click 'Create API Token'"
Write-Host "5. Set label: 'MCP Server Integration'"
Write-Host "6. Copy the generated token"
Write-Host ""

$apiKey = Read-Host "Enter your Plane API token (starts with 'plane_api_')"

if ($apiKey -and $apiKey.StartsWith("plane_api_")) {
    $env:PLANE_API_KEY = $apiKey
    Write-Host "✅ API key set successfully!"
    
    # Test the API key
    Write-Host ""
    Write-Host "Testing API key..."
    try {
        $headers = @{"X-Api-Key" = $apiKey}
        $response = Invoke-WebRequest -Uri "http://localhost:51534/api/workspaces/" -Headers $headers -UseBasicParsing
        Write-Host "✅ API key is valid and working!"
    } catch {
        Write-Host "❌ API key test failed. Error: $($_.Exception.Message)"
    }
} else {
    Write-Host "❌ Invalid API key format. Token should start with 'plane_api_'"
    exit 1
}

# Summary
Write-Host ""
Write-Host "Setup Complete!"
Write-Host "==============="
Write-Host "✅ Plane containers: Running"
Write-Host "✅ Environment variables: Set"
Write-Host "✅ Python dependencies: Installed"
Write-Host "✅ API key: Configured"
Write-Host ""
Write-Host "The MCP server should already be running on port 43533"
Write-Host "If not, start it with: python for_llm/plane-mcp-server.py" 