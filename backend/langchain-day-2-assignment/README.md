# LangChain Assignment Day 2

This folder contains Python solutions for the four LangChain Day-2 tasks from `backend/AssignmentPrompt.txt`.

## Assignment Coverage

| Assignment | File | What it demonstrates |
|---|---|---|
| 1. Self-Correcting Agent | `assignment1_self_correcting_agent.py` | LLM-compatible reasoning, custom SearchTool, custom CalculatorTool, explicit trace |
| 2. Smart Splitter Proof | `assignment2_smart_splitter.py` | `RecursiveCharacterTextSplitter`, `chunk_size=200`, `chunk_overlap=50`, programmatic overlap validation |
| 3. Context Poisoning | `assignment3_context_poisoning.py` | Two contradictory policy documents, embeddings, in-memory vector store, metadata filtering by year |
| 4. Fast & Grounded System | `assignment4_fast_grounded_cache.py` | Strict grounding prompt, exact fallback phrase, Python dictionary cache |

The code uses `python-dotenv` and does not hardcode passwords or API keys.

## Project Files

```text
backend/langchain-day-2-assignment/
├── README.md
├── COMPANY_SERVER_SETUP.md
├── requirements.txt
├── .env.example
├── .gitignore
├── llm_factory.py
├── local_embeddings.py
├── tools.py
├── long_document.txt
├── policy_2022.txt
├── policy_2024.txt
├── assignment1_self_correcting_agent.py
├── assignment2_smart_splitter.py
├── assignment3_context_poisoning.py
├── assignment4_fast_grounded_cache.py
├── run_all.py
└── test_langchain_day2.py
```

## Setup

From the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
cd .\backend\langchain-day-2-assignment
python -m pip install -r requirements.txt
```

Copy the environment template:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env
```

For the company-hosted model server, set `.env` locally like this, replacing placeholder values only on your machine:

```text
LLM_PROVIDER=company
COMPANY_BASE_URL=https://your-company-model-server/v1
COMPANY_MODEL=llama3.1:8b
COMPANY_USERNAME=your_username
COMPANY_PASSWORD=your_password
COMPANY_VERIFY_SSL=false
COMPANY_TIMEOUT=300
USE_LLM_REASONING=false
COST_PER_1000_TOKENS=0
```

Do not commit `.env`.

## Run Tests Without Live LLM Calls

```powershell
python test_langchain_day2.py
```

These tests validate the calculator, search lookup, self-correcting workflow, splitter overlap, metadata filtering, grounding behavior, and caching behavior without making live model API calls.

## Run Each Assignment

Assignment 1:

```powershell
python assignment1_self_correcting_agent.py
```

Expected final trace includes:

```text
Thought 1: The request involves multiplication, but I do not yet know Albert Einstein's birth year, so I must search for that missing fact first.
Action 1: SearchTool: "Albert Einstein birth year"
Observation 1: "1879"
Thought 2: Now that the birth year is 1879, I can pass that value to the CalculatorTool and multiply it by 5.
Action 2: CalculatorTool: "1879 * 5"
Final Answer: 9395
```

Assignment 2:

```powershell
python assignment2_smart_splitter.py
```

This prints Chunk 1, Chunk 2, the extracted 50-character overlap, overlap length, and validation result.

Assignment 3:

```powershell
python assignment3_context_poisoning.py
```

This prints:

```text
User Query: "What is the WFH policy?"
Active Filter: Year: 2024
Retrieved Context: Company WFH Policy: Work from home is allowed 3 days a week.
LLM Final Answer: ...
```

Assignment 4:

```powershell
python assignment4_fast_grounded_cache.py
```

This runs three scenarios:

```text
Scenario 1 (First Ask): valid WFH question calls the LLM or fallback generator
Scenario 2 (Cache Hit): same exact question returns from cache
Scenario 3 (Grounding Test): unrelated chocolate-cake question returns exactly "I do not have enough information"
```

Run all assignments:

```powershell
python run_all.py
```

## Safe ZIP for LMS Upload

Do not upload `.env` because it contains your password. Create a safe ZIP from the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey

$src = ".\backend\langchain-day-2-assignment"
$tmp = ".\backend\langchain-day-2-assignment-submit"
$zip = ".\backend\langchain-day-2-assignment.zip"

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
tar -tf .\backend\langchain-day-2-assignment.zip | Select-String ".env"
```

Seeing `.env.example` is safe. Seeing `.env` is not safe.

Upload:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\backend\langchain-day-2-assignment.zip
```
