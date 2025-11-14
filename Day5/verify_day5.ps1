# Day 5 Verification Script
# Verifies all Day 5 files are present and dependencies are installed

Write-Host "🔍 Day 5 Verification Script" -ForegroundColor Cyan
Write-Host "============================`n" -ForegroundColor Cyan

# Check Day 5a files
Write-Host "📁 Checking Day 5a files..." -ForegroundColor Yellow
$day5a_files = @(
    "5a-agent2agent-communication/01_a2a_server.py",
    "5a-agent2agent-communication/02_a2a_client.py",
    "5a-agent2agent-communication/03_a2a_hybrid.py",
    "5a-agent2agent-communication/README.md",
    "5a-agent2agent-communication/product_catalog_server/__init__.py",
    "5a-agent2agent-communication/product_catalog_server/agent.py",
    "5a-agent2agent-communication/customer_support_client/__init__.py",
    "5a-agent2agent-communication/customer_support_client/agent.py",
    "5a-agent2agent-communication/full_a2a_demo/__init__.py",
    "5a-agent2agent-communication/full_a2a_demo/agent.py"
)

$missing_5a = @()
foreach ($file in $day5a_files) {
    $full_path = Join-Path $PSScriptRoot $file
    if (Test-Path $full_path) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file" -ForegroundColor Red
        $missing_5a += $file
    }
}

# Check Day 5b files
Write-Host "`n📁 Checking Day 5b files..." -ForegroundColor Yellow
$day5b_files = @(
    "5b-agent-deployment/01_deploy_to_agent_engine.py",
    "5b-agent-deployment/02_memory_bank_integration.py",
    "5b-agent-deployment/03_production_config.py",
    "5b-agent-deployment/README.md",
    "5b-agent-deployment/weather_agent_deploy/__init__.py",
    "5b-agent-deployment/weather_agent_deploy/agent.py",
    "5b-agent-deployment/weather_agent_deploy/requirements.txt",
    "5b-agent-deployment/weather_agent_deploy/.env",
    "5b-agent-deployment/weather_agent_deploy/.agent_engine_config.json",
    "5b-agent-deployment/memory_enabled_agent/__init__.py",
    "5b-agent-deployment/memory_enabled_agent/agent.py",
    "5b-agent-deployment/memory_enabled_agent/requirements.txt",
    "5b-agent-deployment/memory_enabled_agent/.env",
    "5b-agent-deployment/memory_enabled_agent/.agent_engine_config.json"
)

$missing_5b = @()
foreach ($file in $day5b_files) {
    $full_path = Join-Path $PSScriptRoot $file
    if (Test-Path $full_path) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file" -ForegroundColor Red
        $missing_5b += $file
    }
}

# Check dependencies
Write-Host "`n📦 Checking Python dependencies..." -ForegroundColor Yellow

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "  ✅ Virtual environment activated: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "     Run: .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
}

# Check google-adk
$adk_check = pip list 2>$null | Select-String "google-adk"
if ($adk_check) {
    Write-Host "  ✅ $adk_check" -ForegroundColor Green
    
    # Check if A2A extras are installed
    $adk_version = pip show google-adk 2>$null | Select-String "Version"
    if ($adk_version) {
        Write-Host "     $adk_version" -ForegroundColor Gray
    }
} else {
    Write-Host "  ❌ google-adk not installed" -ForegroundColor Red
    Write-Host "     Run: pip install -r requirements.txt" -ForegroundColor Gray
}

# Check uvicorn
$uvicorn_check = pip list 2>$null | Select-String "uvicorn"
if ($uvicorn_check) {
    Write-Host "  ✅ $uvicorn_check" -ForegroundColor Green
} else {
    Write-Host "  ❌ uvicorn not installed (required for A2A servers)" -ForegroundColor Red
    Write-Host "     Run: pip install uvicorn>=0.27.0" -ForegroundColor Gray
}

# Check utils package
$utils_check = pip list 2>$null | Select-String "google-adk-course"
if ($utils_check) {
    Write-Host "  ✅ $utils_check (editable install)" -ForegroundColor Green
} else {
    Write-Host "  ❌ utils package not installed" -ForegroundColor Red
    Write-Host "     Run: pip install -e ." -ForegroundColor Gray
}

# Summary
Write-Host "`n📊 Verification Summary" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

$total_files = $day5a_files.Count + $day5b_files.Count
$total_missing = $missing_5a.Count + $missing_5b.Count

Write-Host "Day 5a files: $($day5a_files.Count - $missing_5a.Count)/$($day5a_files.Count) present" -ForegroundColor $(if ($missing_5a.Count -eq 0) { "Green" } else { "Yellow" })
Write-Host "Day 5b files: $($day5b_files.Count - $missing_5b.Count)/$($day5b_files.Count) present" -ForegroundColor $(if ($missing_5b.Count -eq 0) { "Green" } else { "Yellow" })

if ($total_missing -eq 0) {
    Write-Host "`n✅ All Day 5 files present!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Missing $total_missing files" -ForegroundColor Yellow
}

# Next steps
Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Install dependencies: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "2. Test A2A server: python Day5/5a-agent2agent-communication/01_a2a_server.py" -ForegroundColor Gray
Write-Host "3. Test A2A client: python Day5/5a-agent2agent-communication/02_a2a_client.py" -ForegroundColor Gray
Write-Host "4. Review deployment guide: python Day5/5b-agent-deployment/01_deploy_to_agent_engine.py" -ForegroundColor Gray
Write-Host "`nFor detailed testing instructions, see: Day5/DAY5_IMPLEMENTATION_SUMMARY.md`n" -ForegroundColor Gray
