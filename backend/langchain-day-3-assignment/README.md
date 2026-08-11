# LangChain Assignment Day 3

This folder contains Python solutions for the three LangChain Day-3 tasks from `backend/AssignmentPrompt.txt`.

## Assignment Coverage

| Assignment | File | What it demonstrates |
|---|---|---|
| 1. Confused Agent Routing Challenge | `assignment1_confused_agent_routing.py` | Two custom tools, precise docstrings, docstring-guided autonomous routing, no manual if/else routing logic |
| 2. Agent Resilience - Broken API Challenge | `assignment2_agent_resilience.py` | Primary failing stock tool, backup web search tool, recovery trace |
| 3. Lost Context Detective Puzzle | `assignment3_lost_context_rag.py` | `RecursiveCharacterTextSplitter`, chunk overlap, local in-memory vector retrieval, FAISS attempt with memory fallback, grounded final answer |

The code uses `python-dotenv` and does not hardcode passwords or API keys.

## Project Files

```text
backend/langchain-day-3-assignment/
├── README.md
├── COMPANY_SERVER_SETUP.md
├── requirements.txt
├── .env.example
├── .gitignore
├── llm_factory.py
├── local_embeddings.py
├── tools.py
├── assignment1_confused_agent_routing.py
├── assignment2_agent_resilience.py
├── assignment3_lost_context_rag.py
├── run_all.py
└── test_langchain_day3.py
```

## Setup

From the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
cd .\backend\langchain-day-3-assignment
python -m pip install -r requirements.txt
```

Copy the environment template:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env
```

By default, `.env.example` uses:

```text
USE_LIVE_LLM=false
```

That lets the scripts and tests run without calling external APIs. To use the company-hosted model server, see `COMPANY_SERVER_SETUP.md` and set `USE_LIVE_LLM=true` locally.

Do not commit `.env`.

## Run Tests Without Live LLM Calls

```powershell
python test_langchain_day3.py
```

These tests validate:

- cancel vs refund routing
- tool argument extraction
- simulated stock database failure
- backup web search recovery
- splitter behavior
- lost-context retrieval
- exact final answer: `December 31st, 2026, with a $500,000 budget`

## Run Each Assignment

Assignment 1:

```powershell
python assignment1_confused_agent_routing.py
```

Expected routing:

```text
Cancel prompt -> cancel_subscription
Refund prompt -> refund_order
```

Assignment 2:

```powershell
python assignment2_agent_resilience.py
```

Expected trace:

```text
Thought 1: try internal stock database
Action 1: get_internal_stock_price
Observation 1: Error: Database Timeout
Thought 2: recover using backup public web search
Action 2: search_public_web
Final Answer: The current stock price of Apple is $170.
```

Assignment 3:

```powershell
python assignment3_lost_context_rag.py
```

Expected final answer:

```text
December 31st, 2026, with a $500,000 budget
```

The script includes the required multi-line comment at the bottom explaining why `chunk_size=1150` and `chunk_overlap=450` were selected and what goes wrong with too-small overlap.

Run all assignments:

```powershell
python run_all.py
```

## Safe ZIP for LMS Upload

Do not upload `.env` because it can contain your password. Create a safe ZIP from the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey

$src = ".\backend\langchain-day-3-assignment"
$tmp = ".\backend\langchain-day-3-assignment-submit"
$zip = ".\backend\langchain-day-3-assignment.zip"

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $zip -Force -ErrorAction SilentlyContinue
Copy-Item $src $tmp -Recurse

Remove-Item "$tmp\.env" -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\.venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\venv" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem $tmp -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem $tmp -Recurse -File -Filter "*.pyc" | Remove-Item -Force

Compress-Archive -Path $tmp -DestinationPath $zip -Force
Remove-Item $tmp -Recurse -Force
```

Verify `.env` is not included:

```powershell
tar -tf .\backend\langchain-day-3-assignment.zip | Select-String ".env"
```

Seeing `.env.example` is safe. Seeing `.env` is not safe.

Upload:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\backend\langchain-day-3-assignment.zip
```
