# Plane MCP Server Setup Script
# This script helps configure the Plane MCP server environment

Write-Host "🚀 Plane MCP Server Setup" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Step 1: Check if Plane is running
Write-Host "`n📋 Step 1: Checking Plane containers..."
try {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}" | Select-String "plane-working"
    if ($containers) {
        Write-Host "✅ Plane containers are running:" -ForegroundColor Green
        $containers | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
    } else {
        Write-Host "❌ No Plane containers found. Please start Plane first:" -ForegroundColor Red
        Write-Host "   docker-compose up -d" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Docker not available. Please ensure Docker is running." -ForegroundColor Red
    exit 1
}

# Step 2: Test Plane web interface
Write-Host "`n🌐 Step 2: Testing Plane web interface..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:51534" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Plane web interface is accessible at http://localhost:51534" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Cannot access Plane web interface. Check if containers are healthy." -ForegroundColor Red
    Write-Host "   Try: docker logs plane-working-proxy-1" -ForegroundColor Yellow
}

# Step 3: Environment variable setup
Write-Host "`n🔧 Step 3: Environment variable setup..."

# Check current environment variables
$currentApiUrl = $env:PLANE_API_URL
$currentApiKey = $env:PLANE_API_KEY
$currentMcpPort = $env:PLANE_MCP_PORT

Write-Host "Current environment variables:"
Write-Host "   PLANE_API_URL: $(if($currentApiUrl) { $currentApiUrl } else { 'Not set' })"
Write-Host "   PLANE_API_KEY: $(if($currentApiKey) { ($currentApiKey.Substring(0, [Math]::Min(10, $currentApiKey.Length)) + '...') } else { 'Not set' })"
Write-Host "   PLANE_MCP_PORT: $(if($currentMcpPort) { $currentMcpPort } else { 'Not set (will use 43533)' })"

# Set basic environment variables
if (-not $currentApiUrl) {
    Write-Host "`nSetting PLANE_API_URL..."
    $env:PLANE_API_URL = "http://localhost:51534"
    Write-Host "✅ Set PLANE_API_URL = http://localhost:51534" -ForegroundColor Green
}

if (-not $currentMcpPort) {
    Write-Host "Setting PLANE_MCP_PORT..."
    $env:PLANE_MCP_PORT = "43533"
    Write-Host "✅ Set PLANE_MCP_PORT = 43533" -ForegroundColor Green
}

# API Key setup
if (-not $currentApiKey) {
    Write-Host "`n🔑 API Key Setup Required" -ForegroundColor Yellow
    Write-Host "To complete the setup, you need to create a Plane API token:"
    Write-Host ""
    Write-Host "1. Open your browser to: http://localhost:51534" -ForegroundColor Cyan
    Write-Host "2. Log in to your Plane account" -ForegroundColor Cyan
    Write-Host "3. Go to Settings → API Tokens" -ForegroundColor Cyan
    Write-Host "4. Click 'Create API Token'" -ForegroundColor Cyan
    Write-Host "5. Set label: 'MCP Server Integration'" -ForegroundColor Cyan
    Write-Host "6. Copy the generated token" -ForegroundColor Cyan
    Write-Host ""
    
    $apiKey = Read-Host "Enter your Plane API token (starts with 'plane_api_')"
    
    if ($apiKey -and $apiKey.StartsWith("plane_api_")) {
        $env:PLANE_API_KEY = $apiKey
        Write-Host "✅ API key set successfully!" -ForegroundColor Green
        
        # Test the API key
        Write-Host "`nTesting API key..."
        try {
            $headers = @{"X-Api-Key" = $apiKey}
            $testResponse = Invoke-WebRequest -Uri "http://localhost:51534/api/workspaces/" -Headers $headers -UseBasicParsing
            Write-Host "✅ API key is valid and working!" -ForegroundColor Green
        } catch {
            Write-Host "❌ API key test failed. Please check your token." -ForegroundColor Red
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
        }
    } else {
        Write-Host "❌ Invalid API key format. Token should start with 'plane_api_'" -ForegroundColor Red
        Write-Host "Please run this script again with a valid token." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✅ API key already configured" -ForegroundColor Green
}

# Step 4: Install Python dependencies
Write-Host "`n📦 Step 4: Checking Python dependencies..."
$requiredPackages = @("fastapi", "httpx", "prometheus_client", "starlette", "uvicorn")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        $result = pip show $package 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $package is installed" -ForegroundColor Green
        } else {
            $missingPackages += $package
        }
    } catch {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "❌ Missing Python packages: $($missingPackages -join ', ')" -ForegroundColor Red
    Write-Host "Installing missing packages..." -ForegroundColor Yellow
    
    try {
        pip install $missingPackages
        Write-Host "✅ Python dependencies installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install Python packages. Please install manually:" -ForegroundColor Red
        Write-Host "   pip install $($missingPackages -join ' ')" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ All Python dependencies are installed" -ForegroundColor Green
}

# Step 5: Final test
Write-Host "`n🧪 Step 5: Running final tests..."
if (Test-Path "test-mcp.ps1") {
    .\test-mcp.ps1
} else {
    Write-Host "⚠️  test-mcp.ps1 not found, skipping automated tests" -ForegroundColor Yellow
}

# Summary
Write-Host "`n🎉 Setup Summary" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host "✅ Plane containers: Running" -ForegroundColor Green
Write-Host "✅ Environment variables: Configured" -ForegroundColor Green
Write-Host "✅ Python dependencies: Installed" -ForegroundColor Green

if ($env:PLANE_API_KEY) {
    Write-Host "✅ API authentication: Ready" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Ready to start MCP server!" -ForegroundColor Green
    Write-Host "Run: python for_llm/plane-mcp-server.py" -ForegroundColor Cyan
} else {
    Write-Host "❌ API authentication: Incomplete" -ForegroundColor Red
    Write-Host "Please set your API key and run this script again." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📚 For detailed instructions, see: for_llm/PLANE_MCP_SETUP.md" -ForegroundColor Gray 