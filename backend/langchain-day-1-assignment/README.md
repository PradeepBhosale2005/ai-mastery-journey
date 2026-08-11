# LangChain Assignment Day 1

This folder contains complete Python solutions for the four LangChain Day-1 tasks from `backend/AssignmentPrompt.txt`.

## Assignment Coverage

| Assignment | File | What it demonstrates |
|---|---|---|
| 1. Messy Data Cleaner | `assignment1_messy_data_cleaner.py` | `PromptTemplate`, LLM wrapper, `StrOutputParser` |
| 2. Marketing Assembly Line | `assignment2_marketing_assembly_line.py` | Two-step LCEL chain using the pipe operator `|` |
| 3. Mini-RAG | `assignment3_mini_rag.py` | Document loader, text splitter, embeddings, in-memory vector retrieval, RAG prompt |
| 4. Watchful Eye | `assignment4_token_receipt.py` | LangChain callback/token counter and formatted token/cost receipt |

The code uses `python-dotenv` and does not hardcode API keys.

## Project Files

```text
backend/langchain-day-1-assignment/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── game_rules.txt
├── llm_factory.py
├── local_embeddings.py
├── assignment1_messy_data_cleaner.py
├── assignment2_marketing_assembly_line.py
├── assignment3_mini_rag.py
├── assignment4_token_receipt.py
├── run_all.py
└── test_langchain_day1.py
```

## Setup

From the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
cd .\backend\langchain-day-1-assignment
python -m pip install -r requirements.txt
```

If your Python 3.14 environment has package issues, install and use Python 3.12 or 3.13, then run the same commands with `py -3.12` or `py -3.13`.

## Configure Environment

Copy the example environment file:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env
```

Default configuration uses local Ollama:

```text
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

For local Ollama, install Ollama and pull a small model:

```powershell
ollama pull llama3.1:8b
```

Do not commit `.env`. It is ignored by `.gitignore`.

## Run Each Assignment

Assignment 1:

```powershell
python assignment1_messy_data_cleaner.py
```

Expected output format:

```text
Sentiment: Negative, Core Issue: Blender lid flew off while making a smoothie and caused a mess/refund request.
```

Assignment 2:

```powershell
python assignment2_marketing_assembly_line.py "EcoBottle"
```

This generates a five-word English slogan and translates it into French using an LCEL pipe sequence.

Assignment 3:

```powershell
python assignment3_mini_rag.py
```

This loads `game_rules.txt`, chunks it, embeds chunks with a local deterministic embedding class, stores/retrieves them in memory, and asks the LLM to answer the golden-token question.

Assignment 4:

```powershell
python assignment4_token_receipt.py
```

For OpenAI, it attempts to use LangChain's OpenAI callback. For Ollama/Gemini/local models, it uses a custom LangChain callback handler to estimate prompt tokens, completion tokens, total tokens, and cost.

Run all tasks:

```powershell
python run_all.py
```

## Run Tests Without Live LLM Calls

```powershell
python test_langchain_day1.py
```

These tests validate prompt variables, local embeddings, retrieval behavior, and the token counter without making live model API calls.

## Safe ZIP for LMS Upload

Do not upload `.env` or cache files. Create a safe ZIP from the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey

$src = ".\backend\langchain-day-1-assignment"
$tmp = ".\backend\langchain-day-1-assignment-submit"
$zip = ".\backend\langchain-day-1-assignment.zip"

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $zip -Force -ErrorAction SilentlyContinue
Copy-Item $src $tmp -Recurse

Remove-Item "$tmp\.env" -Force -ErrorAction SilentlyContinue
Get-ChildItem $tmp -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem $tmp -Recurse -File -Filter "*.pyc" | Remove-Item -Force

Compress-Archive -Path $tmp -DestinationPath $zip -Force
Remove-Item $tmp -Recurse -Force
```

Upload:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\backend\langchain-day-1-assignment.zip
```
