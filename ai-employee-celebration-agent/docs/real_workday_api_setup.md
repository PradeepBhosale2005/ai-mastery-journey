# Real Workday API Integration Setup

This project now supports real Workday employee data through a configurable Workday RaaS JSON endpoint.

## Recommended Integration Pattern

Use a Workday custom report exposed as **Report-as-a-Service (RaaS)** with JSON output.

The report should return these columns:

| App Field | Recommended Workday Report Column |
|---|---|
| employee_id | Employee_ID |
| worker_id | Worker_ID |
| preferred_name | Preferred_Name |
| legal_name | Legal_Name |
| email | Work_Email |
| manager_email | Manager_Email |
| date_of_birth | Date_of_Birth |
| hire_date | Hire_Date |
| timezone | Time_Zone |
| country | Country |
| department | Department |
| status | Worker_Status |
| celebration_channel | Celebration_Channel |

Date columns should be returned in `YYYY-MM-DD` format.

## Local Configuration

Copy the real API example file:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey\ai-employee-celebration-agent
Copy-Item .\.env.real.example .\.env
notepad .\.env
```

Fill only your local `.env` file. Do not commit it.

Minimum required values:

```text
WORKDAY_RAAS_URL=https://...your Workday RaaS JSON URL...
WORKDAY_USERNAME=your_isu_username
WORKDAY_PASSWORD=your_isu_password
WORKDAY_VERIFY_SSL=true
```

If your tenant uses bearer token access, use:

```text
WORKDAY_ACCESS_TOKEN=your_access_token
```

When `WORKDAY_ACCESS_TOKEN` is supplied, the client uses bearer token authentication instead of Basic Auth.

## Test Connection

```powershell
python scripts\test_real_workday_connection.py
```

This prints a safe preview without exposing full birth dates or credentials.

## Run Agent With Real Workday Data

```powershell
python run_real_workday_agent.py --date 2026-08-30
```

Output files:

```text
outbox/real_workday_notifications.jsonl
audit_logs/real_workday_agent_audit.jsonl
```

## Real LLM Later

Keep this first real Workday test in mock LLM mode:

```text
LLM_PROVIDER=mock
```

After Workday data is confirmed, set the company LLM values in `.env` and run again.

## Important Security Notes

- Do not commit `.env`.
- Do not paste passwords or tokens into chat.
- Use a read-only ISU for the RaaS report.
- Expose only the fields required by this MVP.
- For public celebration posts, consider HR approval before publishing.
