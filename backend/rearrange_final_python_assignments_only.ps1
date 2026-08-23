$ErrorActionPreference = "Stop"

# Purpose:
# Rearrange already-completed Python assignments into one final reference folder.
# No extra README is created because each assignment folder already has its own README.
#
# Run from repo root:
# powershell -ExecutionPolicy Bypass -File .\backend\rearrange_final_python_assignments_only.ps1

$backendDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $backendDir
$destRoot = Join-Path $backendDir "final all python Assignment"
$zipPath = Join-Path $backendDir "final all python Assignment.zip"

$assignments = @(
    @{
        Source = "hello-world-python"
        Target = "Assignment 01 - Hello World Python"
    },
    @{
        Source = "python-dsa-problems"
        Target = "Assignment 02 - Python DSA Problems"
    },
    @{
        Source = "python-oop-assignment"
        Target = "Assignment 03 - Python OOP Concepts"
    },
    @{
        Source = "python-numpy-assignment-04"
        Target = "Assignment 04 - NumPy Assignment"
    },
    @{
        Source = "python-pandas-assignment-05"
        Target = "Assignment 05 - Pandas Assignment"
    }
)

Write-Host "Rearranging completed Python assignments..." -ForegroundColor Cyan
Write-Host "Final folder: $destRoot" -ForegroundColor Cyan

if (Test-Path $destRoot) {
    Remove-Item $destRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $destRoot | Out-Null

foreach ($assignment in $assignments) {
    $sourcePath = Join-Path $repoRoot $assignment.Source
    $targetPath = Join-Path $destRoot $assignment.Target

    if (-not (Test-Path $sourcePath)) {
        throw "Missing source folder: $sourcePath"
    }

    Write-Host "Copying: $($assignment.Source) -> $($assignment.Target)" -ForegroundColor Green
    Copy-Item $sourcePath $targetPath -Recurse -Force
}

# Remove runtime/cache/sensitive/generated files from copied folders only.
$removeDirectories = @("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".venv", "venv", "env", "logs", "dist", "build")
foreach ($dirName in $removeDirectories) {
    Get-ChildItem $destRoot -Recurse -Directory -Filter $dirName -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

$removeFiles = @("*.pyc", "*.pyo", "*.zip", ".env", "local_model_config.txt", "local_llama_config.txt", "*.log")
foreach ($filePattern in $removeFiles) {
    Get-ChildItem $destRoot -Recurse -File -Filter $filePattern -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
}

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Compress-Archive -Path $destRoot -DestinationPath $zipPath -Force

Write-Host ""
Write-Host "Done. Rearranged folders:" -ForegroundColor Green
Get-ChildItem $destRoot -Directory | Sort-Object Name | ForEach-Object { Write-Host "- $($_.Name)" }
Write-Host ""
Write-Host "ZIP created:" -ForegroundColor Green
Write-Host $zipPath
