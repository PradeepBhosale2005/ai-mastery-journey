# Company-hosted model setup

Use this option when local Ollama is not installed or corporate security blocks external SaaS providers.

1. Copy `.env.example` to `.env`.
2. Replace placeholder values locally.
3. Do not commit `.env`.

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

Example commands:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env
python assignment1_self_correcting_agent.py
python assignment2_smart_splitter.py
python assignment3_context_poisoning.py
python assignment4_fast_grounded_cache.py
```
