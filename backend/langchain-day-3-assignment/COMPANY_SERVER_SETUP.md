# Company Server Setup

Use this only when you want the scripts to call a live company-hosted OpenAI-compatible model.

The default assignment scripts run with `USE_LIVE_LLM=false`, so they can demonstrate the required workflows without external API calls. To use a live model, copy `.env.example` to `.env` and set values locally.

```text
LLM_PROVIDER=company
USE_LIVE_LLM=true
COMPANY_BASE_URL=https://your-company-model-server/v1
COMPANY_MODEL=llama3.1:8b
COMPANY_USERNAME=your_username
COMPANY_PASSWORD=your_password
COMPANY_VERIFY_SSL=false
COMPANY_TIMEOUT=300
```

Do not commit `.env` because it contains your password.

Run examples:

```powershell
python assignment1_confused_agent_routing.py
python assignment2_agent_resilience.py
python assignment3_lost_context_rag.py
```
