# Auto DataDash - Windows PowerShell One-Click Setup & Launch Script
# Run in PowerShell: .\setup.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Auto DataDash - Setup & Launch Script   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
Write-Host "`n[1/4] Checking Python installation..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  [!] Python is not found in PATH." -ForegroundColor Red
    Write-Host "  Install via winget: winget install Python.Python.3.11" -ForegroundColor Yellow
    exit 1
}

# 2. Virtual Environment Setup
Write-Host "`n[2/4] Setting up Python virtual environment (venv)..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "  Created virtual environment in .\venv" -ForegroundColor Green
} else {
    Write-Host "  Virtual environment already exists in .\venv" -ForegroundColor Green
}

# 3. Install Requirements
Write-Host "`n[3/4] Installing Python requirements..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\venv\Scripts\pip.exe" install -r requirements.txt
Write-Host "  Dependencies installed successfully!" -ForegroundColor Green

# 4. Launch Application
Write-Host "`n[4/4] Starting Auto DataDash Python Server..." -ForegroundColor Yellow
Write-Host "  Serving at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "  Press Ctrl+C to stop the server.`n" -ForegroundColor Gray

# Open browser automatically after 1 second
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 1
    Start-Process "http://localhost:5000"
} | Out-Null

# Run Server
& ".\venv\Scripts\python.exe" server.py
