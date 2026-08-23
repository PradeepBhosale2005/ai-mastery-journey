$ErrorActionPreference = "Stop"

# This script creates a final submission folder for the Python assignments listed in:
# backend/Python all assignment .txt
#
# Run from any location after git pull:
# powershell -ExecutionPolicy Bypass -File .\backend\create_final_all_python_assignment.ps1

$backendDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $backendDir
$destRoot = Join-Path $backendDir "final all python Assignment"
$zipPath = Join-Path $backendDir "final all python Assignment.zip"

$assignments = @(
    @{
        Number = "01"
        Title = "Hello World Python"
        Source = "hello-world-python"
        Target = "Assignment 01 - Hello World Python"
        Notes = "Dev environment, Git repo, Hello World, README"
    },
    @{
        Number = "02"
        Title = "Python DSA Problems"
        Source = "python-dsa-problems"
        Target = "Assignment 02 - Python DSA Problems"
        Notes = "Array, string, stack, hashing, and algorithm practice problems"
    },
    @{
        Number = "03"
        Title = "Python OOP Concepts"
        Source = "python-oop-assignment"
        Target = "Assignment 03 - Python OOP Concepts"
        Notes = "Class, inheritance, encapsulation, polymorphism, abstraction"
    },
    @{
        Number = "04"
        Title = "NumPy Assignment"
        Source = "python-numpy-assignment-04"
        Target = "Assignment 04 - NumPy Assignment"
        Notes = "Array creation, slicing, broadcasting, statistics, linear algebra"
    },
    @{
        Number = "05"
        Title = "Pandas Assignment"
        Source = "python-pandas-assignment-05"
        Target = "Assignment 05 - Pandas Assignment"
        Notes = "Completed numbered Assignment 05 folder in the repo. The source prompt repeats Assignment 04 content under Assignment 05."
    }
)

Write-Host "Creating final Python assignment folder..." -ForegroundColor Cyan
Write-Host "Destination: $destRoot" -ForegroundColor Cyan

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

    Write-Host "Copying $($assignment.Target)" -ForegroundColor Green
    Copy-Item $sourcePath $targetPath -Recurse -Force
}

# Remove runtime, cache, local credential, and generated files from the final package.
$removeDirectories = @("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".venv", "venv", "env", "logs", "dist", "build")
foreach ($dirName in $removeDirectories) {
    Get-ChildItem $destRoot -Recurse -Directory -Filter $dirName -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

$removeFiles = @("*.pyc", "*.pyo", "*.zip", ".env", "local_model_config.txt", "local_llama_config.txt", "*.log")
foreach ($filePattern in $removeFiles) {
    Get-ChildItem $destRoot -Recurse -File -Filter $filePattern -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
}

$readmePath = Join-Path $destRoot "README.md"
@"
# Final All Python Assignment

This folder was generated from `backend/Python all assignment .txt`.

## Included Assignments

| Assignment | Final Folder | Source Folder | Status |
|---|---|---|---|
| 01 | Assignment 01 - Hello World Python | hello-world-python | Completed |
| 02 | Assignment 02 - Python DSA Problems | python-dsa-problems | Completed |
| 03 | Assignment 03 - Python OOP Concepts | python-oop-assignment | Completed |
| 04 | Assignment 04 - NumPy Assignment | python-numpy-assignment-04 | Completed |
| 05 | Assignment 05 - Pandas Assignment | python-pandas-assignment-05 | Completed |

## Note

The source file repeats the NumPy assignment content under Assignment 5. The completed numbered Assignment 05 folder in this repository is `python-pandas-assignment-05`, so it is included as Assignment 05 in this final package.

## Safety

Runtime folders, cache folders, zip files, `.env`, `local_model_config.txt`, and `local_llama_config.txt` are removed from this final package.
"@ | Set-Content -Path $readmePath -Encoding UTF8

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Compress-Archive -Path $destRoot -DestinationPath $zipPath -Force

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "Final folder: $destRoot" -ForegroundColor Green
Write-Host "Final ZIP:    $zipPath" -ForegroundColor Green
Write-Host ""
Write-Host "Included folders:" -ForegroundColor Cyan
Get-ChildItem $destRoot -Directory | Sort-Object Name | ForEach-Object { Write-Host "- $($_.Name)" }
