# AI Employee Birthday & Work Anniversary Celebration Agent

## AI Agent Use Case Name Selected from LMS

**AI Employee Birthday & Work Anniversary Celebration Agent**

This project implements the LMS AI Agent use case where an agent integrates with Workday-style employee data to identify birthdays and work anniversaries, checks employee status and timezone, generates personalized Gen-AI messages, and prepares Email or Jadean Jar celebration notifications.

## Business Problem

HR teams often track employee birthdays and work anniversaries manually. This creates missed celebrations, inconsistent messages, and repeated administrative effort.

This AI agent automates the process while keeping the workflow auditable and easy to review.

## MVP Features

- Mock Workday employee API using JSON data
- Active employee validation
- Timezone-aware local date check
- Birthday detection
- Work anniversary detection
- AI message generation using mock mode by default
- Optional OpenAI-compatible/company LLM call through environment variables
- Email and Jadean Jar notification simulation
- JSONL audit log
- Streamlit demo dashboard
- Unit tests

## Project Structure

```text
ai-employee-celebration-agent/
├── README.md
├── SUBMISSION.md
├── app.py
├── run_daily_agent.py
├── requirements.txt
├── .env.example
├── data/
│   └── mock_workday_employees.json
├── docs/
│   └── architecture.md
├── scripts/
│   └── prepare_separate_repo.ps1
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── audit_logger.py
│   ├── celebration_detector.py
│   ├── message_generator.py
│   ├── models.py
│   ├── notification_service.py
│   └── workday_client.py
└── tests/
    ├── test_agent.py
    ├── test_celebration_detector.py
    └── test_message_generator.py
```

## Setup

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
cd .\ai-employee-celebration-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the CLI Demo

The sample data contains birthday and anniversary events on `2026-08-29`.

```powershell
python run_daily_agent.py --date 2026-08-29
```

Output files are generated locally:

```text
outbox/notifications.jsonl
audit_logs/agent_audit.jsonl
```

These generated folders are ignored by Git.

## Run the Streamlit UI

```powershell
streamlit run app.py
```

Use `2026-08-29` as the business date to see demo events.

## Run Tests

```powershell
python -m pytest tests
```

## Optional Company LLM Configuration

The project runs in mock mode by default, so no credentials are needed.

To use an OpenAI-compatible/company LLM, copy `.env.example` to `.env` and configure:

```text
LLM_PROVIDER=company
LLM_BASE_URL=https://your-llm-server/v1
LLM_MODEL=llama3.1:8b
LLM_USERNAME=your_username
LLM_PASSWORD=your_password
LLM_VERIFY_SSL=false
```

Do not commit `.env` or real credentials.

## Separate Git Repo Submission

The LMS asks for a separate Git repository. Use the helper script:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
powershell -ExecutionPolicy Bypass -File .\ai-employee-celebration-agent\scripts\prepare_separate_repo.ps1
```

Then create an empty GitHub repo named:

```text
ai-employee-celebration-agent
```

Push the prepared standalone folder:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-employee-celebration-agent
git branch -M main
git remote add origin https://github.com/<your-username>/ai-employee-celebration-agent.git
git push -u origin main
```

## Demo Checklist

```text
1. Open Streamlit UI.
2. Select business date 2026-08-29.
3. Run the agent.
4. Confirm active employee birthdays and anniversaries are detected.
5. Confirm inactive employees are skipped.
6. Review generated AI messages.
7. Review outbox/notifications.jsonl.
8. Review audit_logs/agent_audit.jsonl.
```

## Future Enhancements

- Replace mock data with real Workday REST/SOAP/RaaS integration
- Add real Microsoft Graph or SMTP email delivery
- Add real Jadean Jar API integration
- Add HR approval workflow before public posts
- Add scheduler using Windows Task Scheduler, cron, or GitHub Actions
