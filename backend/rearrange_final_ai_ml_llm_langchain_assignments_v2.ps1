$ErrorActionPreference = "Stop"

# Purpose:
# Rearrange completed AI-ML, LLM, and LangChain assignments into final reference
# folders for sharing with colleagues.
#
# No extra README is created in the final folders. Each assignment folder already
# contains its own README.
#
# Run from repo root:
# powershell -ExecutionPolicy Bypass -File .\backend\rearrange_final_ai_ml_llm_langchain_assignments_v2.ps1

$backendDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $backendDir

$categories = @(
    @{
        Name = "AI-ML"
        DestFolder = "final all AI-ML Assignment"
        ZipName = "final all AI-ML Assignment.zip"
        Completed = @(
            @{ Source = "python-linear-regression-assignment-06"; Target = "Assignment 01 - Linear Regression" },
            @{ Source = "ai-ml-assignment-02-titanic-preprocessing"; Target = "Assignment 02 - Titanic Preprocessing Pipeline" },
            @{ Source = "ai-ml-assignment-03-breast-cancer-logistic-regression"; Target = "Assignment 03 - Breast Cancer Logistic Regression" },
            @{ Source = "ai-ml-assignment-04-pytorch-iris-mlp"; Target = "Assignment 04 - PyTorch Iris MLP" },
            @{ Source = "ai-ml-assignment-05-pytorch-digits-mlp"; Target = "Assignment 05 - PyTorch Digits MLP" }
        )
    },
    @{
        Name = "LLM"
        DestFolder = "final all LLM Assignment"
        ZipName = "final all LLM Assignment.zip"
        Completed = @(
            @{ Source = "python-tokenizer-assignment-07"; Target = "Assignment 01 - Tokenizer and Vocabulary" },
            @{ Source = "python-article-analysis-llm-assignment-08"; Target = "Assignment 02 - Article Analysis LLM" },
            @{ Source = "python-multi-model-interaction-assignment-09"; Target = "Assignment 03 - Multi-Model Interaction" },
            @{ Source = "llm-assignment-04-lora-qlora-finetuning"; Target = "Assignment 04 - LoRA and QLoRA Fine-Tuning" },
            @{ Source = "python-multi-model-adversarial-reasoning-assignment-10"; Target = "Assignment 05 - Multi-Model Adversarial Reasoning" }
        )
    },
    @{
        Name = "LangChain"
        DestFolder = "final all LangChain Assignment"
        ZipName = "final all LangChain Assignment.zip"
        Completed = @(
            @{ Source = "backend\langchain-day-1-assignment"; Target = "Assignment 01 - LangChain Day 1" },
            @{ Source = "backend\langchain-day-2-assignment"; Target = "Assignment 02 - LangChain Day 2" },
            @{ Source = "backend\langchain-day-3-assignment"; Target = "Assignment 03 - LangChain Day 3" }
        )
    }
)

function Remove-RuntimeFiles {
    param([string]$Path)

    $removeDirectories = @(
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints",
        ".venv", "venv", "env", "logs", "dist", "build", "node_modules", "coverage",
        "output_reports", "outputs", "results", "adapters"
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

    $missing = @()
    foreach ($assignment in $category.Completed) {
        $sourcePath = Join-Path $repoRoot $assignment.Source
        $targetPath = Join-Path $destRoot $assignment.Target

        if (-not (Test-Path $sourcePath)) {
            $missing += $assignment.Source
            continue
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

    if ($missing.Count -gt 0) {
        Write-Host "Missing source folders for $($category.Name):" -ForegroundColor Yellow
        foreach ($item in $missing) {
            Write-Host "- $item" -ForegroundColor Yellow
        }
    } else {
        Write-Host "All $($category.Name) assignments were rearranged." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green
