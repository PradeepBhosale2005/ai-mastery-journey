param(
    [string]$OutputZip = ""
)

$ErrorActionPreference = "Stop"

$scriptDir = $PSScriptRoot
$projectRoot = Split-Path -Parent $scriptDir
$projectName = Split-Path -Leaf $projectRoot
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

if ([string]::IsNullOrWhiteSpace($OutputZip)) {
    $OutputZip = Join-Path (Split-Path -Parent $projectRoot) "$projectName-submission-$timestamp.zip"
}

$tempRoot = Join-Path $env:TEMP "$projectName-submission-$timestamp"
$tempProject = Join-Path $tempRoot $projectName

Write-Host "Preparing clean submission ZIP..." -ForegroundColor Cyan
Write-Host "Source: $projectRoot" -ForegroundColor Cyan
Write-Host "Output: $OutputZip" -ForegroundColor Cyan

if (Test-Path $tempRoot) {
    Remove-Item $tempRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $tempRoot | Out-Null

Copy-Item $projectRoot $tempProject -Recurse -Force

$removeDirs = @(
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    "outbox",
    "audit_logs",
    "logs",
    ".mypy_cache",
    ".ruff_cache"
)

foreach ($dirName in $removeDirs) {
    Get-ChildItem $tempProject -Recurse -Directory -Filter $dirName -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

$removeFiles = @(
    ".env",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.zip",
    ".DS_Store",
    "Thumbs.db"
)

foreach ($filePattern in $removeFiles) {
    Get-ChildItem $tempProject -Recurse -File -Filter $filePattern -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
}

if (Test-Path $OutputZip) {
    Remove-Item $OutputZip -Force
}

Compress-Archive -Path (Join-Path $tempProject "*") -DestinationPath $OutputZip -Force
Remove-Item $tempRoot -Recurse -Force

Write-Host ""
Write-Host "Submission ZIP created successfully:" -ForegroundColor Green
Write-Host $OutputZip -ForegroundColor Green
Write-Host ""
Write-Host "Before uploading, confirm that the ZIP does not contain .env, passwords, audit logs, outbox data, or virtual environment folders." -ForegroundColor Yellow
