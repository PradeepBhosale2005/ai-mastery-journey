# LangGraph Assignment 02: AI Document Processing Workflow

This folder contains a complete LangGraph solution for the AI Document Processing Workflow assignment from `backend/AssignmentPrompt.txt`.

## Assignment Requirement

Build a LangGraph-based workflow system that processes a Software Requirement Document (SRS) and produces structured insights.

The workflow must use multiple agents and workflow orchestration to:

1. Analyze the SRS document.
2. Extract requirements.
3. Identify risks.
4. Suggest architecture.
5. Generate test cases.
6. Merge all outputs.
7. Include a Human Review / HITL step.
8. Produce a final report.

## Implemented Graph

```text
START
  |
  v
Input SRS
  |
  v
Document Analyzer
  |----------------------|
  v                      v
Requirement Agent        Risk Agent
  |                      |
  v                      v
Architecture Agent       Test Case Agent
  |                      |
  |----------|-----------|
             v
       Merge Results
             |
             v
       Human Review HITL
             |
             v
       Final Report
             |
             v
            END
```

## Project Files

```text
backend/langgraph-assignment-02-ai-document-processing/
├── README.md
├── requirements.txt
├── .gitignore
├── sample_srs.md
├── state_schema.py
├── agents.py
├── document_workflow.py
├── main.py
├── run_examples.py
└── test_document_workflow.py
```

## Setup

From the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
cd .\backend\langgraph-assignment-02-ai-document-processing
python -m pip install -r requirements.txt
```

## Run the Workflow

Run with the bundled sample SRS:

```powershell
python main.py
```

Run and show workflow trace:

```powershell
python main.py --show-trace
```

Save the final report:

```powershell
python main.py --output output_reports\final_report.md
```

Run with a custom SRS file:

```powershell
python main.py --file path\to\your_srs.md
```

Run the example script:

```powershell
python run_examples.py
```

## Run Tests

```powershell
python test_document_workflow.py
```

The tests validate:

- graph compilation
- requirement extraction
- all assignment nodes execute
- requirement/risk/architecture/test outputs are merged
- Human Review HITL status is present
- final report is generated
- validation errors are created for empty documents

## Safe ZIP for LMS Upload

Create a safe ZIP from the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey

$src = ".\backend\langgraph-assignment-02-ai-document-processing"
$tmp = ".\backend\langgraph-assignment-02-ai-document-processing-submit"
$zip = ".\backend\langgraph-assignment-02-ai-document-processing.zip"

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $zip -Force -ErrorAction SilentlyContinue
Copy-Item $src $tmp -Recurse

Remove-Item "$tmp\.env" -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\.venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\output_reports" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem $tmp -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem $tmp -Recurse -File -Filter "*.pyc" | Remove-Item -Force

Compress-Archive -Path $tmp -DestinationPath $zip -Force
Remove-Item $tmp -Recurse -Force
```

Verify the ZIP does not contain runtime files:

```powershell
tar -tf .\backend\langgraph-assignment-02-ai-document-processing.zip | Select-String ".env|__pycache__|output_reports"
```

No output means it is safe.

Upload:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\backend\langgraph-assignment-02-ai-document-processing.zip
```
