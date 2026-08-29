param(
    [string]$Destination = "C:\Users\pradeep.bhosale_jade\ai-employee-celebration-agent"
)

$ErrorActionPreference = "Stop"

$scriptDir = $PSScriptRoot
$projectRoot = Split-Path -Parent $scriptDir

Write-Host "Preparing standalone repo folder..." -ForegroundColor Cyan
Write-Host "Source:      $projectRoot" -ForegroundColor Cyan
Write-Host "Destination: $Destination" -ForegroundColor Cyan

if (Test-Path $Destination) {
    Remove-Item $Destination -Recurse -Force
}

Copy-Item $projectRoot $Destination -Recurse -Force

$removeDirs = @(".git", ".venv", "venv", "env", "__pycache__", ".pytest_cache", "outbox", "audit_logs")
foreach ($dirName in $removeDirs) {
    Get-ChildItem $Destination -Recurse -Directory -Filter $dirName -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

$removeFiles = @(".env", "*.pyc", "*.pyo", "*.zip", "*.log")
foreach ($filePattern in $removeFiles) {
    Get-ChildItem $Destination -Recurse -File -Filter $filePattern -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
}

Push-Location $Destination
try {
    git init
    git add .
    git commit -m "Initial AI employee celebration agent"
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "Standalone repo is ready:" -ForegroundColor Green
Write-Host $Destination
Write-Host ""
Write-Host "Next create an empty GitHub repo named ai-employee-celebration-agent, then run:" -ForegroundColor Yellow
Write-Host "cd $Destination"
Write-Host "git branch -M main"
Write-Host "git remote add origin https://github.com/<your-username>/ai-employee-celebration-agent.git"
Write-Host "git push -u origin main"
