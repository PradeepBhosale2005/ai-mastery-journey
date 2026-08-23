$ErrorActionPreference = "Stop"

# Purpose:
# Rearrange the completed LangGraph and React assignments into final reference folders
# for sharing with colleagues.
#
# No extra README files are created in final folders. Each assignment folder already
# contains its own README.
#
# Run from repo root:
# powershell -ExecutionPolicy Bypass -File .\backend\rearrange_final_langgraph_react_assignments.ps1

$backendDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $backendDir

$categories = @(
    @{
        Name = "LangGraph"
        DestFolder = "final all LangGraph Assignment"
        ZipName = "final all LangGraph Assignment.zip"
        Completed = @(
            @{ Source = "backend\langgraph-assignment-01-smart-expense"; Target = "Assignment 01 - Smart Expense Processing" },
            @{ Source = "backend\langgraph-assignment-02-ai-document-processing"; Target = "Assignment 02 - AI Document Processing Workflow" }
        )
    },
    @{
        Name = "React"
        DestFolder = "final all React Assignment"
        ZipName = "final all React Assignment.zip"
        Completed = @(
            @{ Source = "frontend\react-smart-task-manager"; Target = "Assignment 01 - Smart Task Manager" }
        )
    }
)

function Remove-RuntimeFiles {
    param([string]$Path)

    $removeDirectories = @(
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints",
        ".venv", "venv", "env", "logs", "dist", "build", "node_modules", "coverage",
        "output_reports", "outputs", "results", ".vite"
    )

    foreach ($dirName in $removeDirectories) {
        Get-ChildItem $Path -Recurse -Directory -Filter $dirName -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }

    $removeFiles = @("*.pyc", "*.pyo", "*.zip", ".env", "local_model_config.txt", "local_llama_config.txt", "*.log")
    foreach ($filePattern in $removeFiles) {
        Get-ChildItem $Path -Recurse -File -Filter $filePattern -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

foreach ($category in $categories) {
    Write-Host ""
    Write-Host "Processing $($category.Name) assignments..." -ForegroundColor Cyan

    $destRoot = Join-Path $backendDir $category.DestFolder
    $zipPath = Join-Path $backendDir $category.ZipName

    if (Test-Path $destRoot) {
        Remove-Item $destRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Path $destRoot | Out-Null

    foreach ($assignment in $category.Completed) {
        $sourcePath = Join-Path $repoRoot $assignment.Source
        $targetPath = Join-Path $destRoot $assignment.Target

        if (-not (Test-Path $sourcePath)) {
            throw "Missing source folder: $sourcePath"
        }

        Write-Host "Copying: $($assignment.Source) -> $($assignment.Target)" -ForegroundColor Green
        Copy-Item $sourcePath $targetPath -Recurse -Force
    }

    Remove-RuntimeFiles -Path $destRoot

    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }
    Compress-Archive -Path $destRoot -DestinationPath $zipPath -Force

    Write-Host "Created folder: $destRoot" -ForegroundColor Green
    Write-Host "Created ZIP:    $zipPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green
