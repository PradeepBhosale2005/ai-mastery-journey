# Company-hosted OpenAI-compatible server setup

Use this option when local Ollama is not installed or corporate security blocks external SaaS providers.

1. Copy this file to `.env`.
2. Replace the placeholder values locally.
3. Do not commit `.env`.

```text
LLM_PROVIDER=company
COMPANY_BASE_URL=https://your-company-model-server/v1
COMPANY_MODEL=llama3.1:8b
COMPANY_USERNAME=your_username
COMPANY_PASSWORD=your_password
COMPANY_VERIFY_SSL=false
COMPANY_TIMEOUT=300
COST_PER_1000_TOKENS=0
```

Example run:

```powershell
python assignment1_messy_data_cleaner.py
python assignment2_marketing_assembly_line.py "EcoBottle"
python assignment3_mini_rag.py
python assignment4_token_receipt.py
```
