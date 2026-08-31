# Operational Agent Setup

This document explains the production-style flow added to the AI Employee Birthday & Work Anniversary Celebration Agent.

## What is included

- Real Workday RaaS report consumption through `RPT_AI_Employee_Celebration_Agent`
- Upcoming birthday and work anniversary preview
- Due-today delivery logic
- Optional delivery for upcoming events
- SMTP email delivery
- Generic API posting for any downstream system
- JSONL outbox and audit trail
- Enhanced Streamlit frontend

## Main commands

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey\ai-employee-celebration-agent
Copy-Item .\.env.operational.example .\.env
notepad .\.env
```

Install dependencies if needed:

```powershell
py -3.14 -m pip install --user -r requirements.txt
```

Test Workday connection:

```powershell
$env:PYTHONPATH = (Get-Location).Path
py -3.14 scripts\test_actual_workday_report_connection.py
```

Run operational CLI in dry run mode:

```powershell
py -3.14 run_operational_agent.py --date 2027-05-25 --lookahead-days 30
```

Run enhanced frontend:

```powershell
py -3.14 -m streamlit run app_operational.py
```

## Delivery safety model

The agent is safe by default.

- `dry_run=True` by default
- SMTP does not send unless `--no-dry-run --send-email` is used
- API does not post unless `--no-dry-run --post-api` is used
- Upcoming events are previewed, but only due-today events are delivered by default
- To deliver upcoming events too, use `--notify-upcoming`

## SMTP setup

Use test mode first:

```text
SMTP_ENABLED=true
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_user
SMTP_PASSWORD=your_smtp_password
SMTP_FROM_EMAIL=celebrations@example.com
SMTP_FROM_NAME=AI Celebration Agent
SMTP_USE_TLS=true
SMTP_TO_OVERRIDE=your.test.email@example.com
SMTP_CC_MANAGER=false
```

With `SMTP_TO_OVERRIDE`, every email goes to your test address instead of the employee. Remove it only after testing.

Run real SMTP delivery for due-today events:

```powershell
py -3.14 run_operational_agent.py --date 2027-05-25 --send-email --no-dry-run
```

## Generic API posting

The project can post the same celebration payload to any API/webhook that accepts JSON.

```text
POST_TARGET_API_ENABLED=true
POST_TARGET_API_URL=https://example.com/api/celebrations
POST_TARGET_API_METHOD=POST
POST_TARGET_API_BEARER_TOKEN=
POST_TARGET_API_HEADERS_JSON={"X-Source":"AI-Celebration-Agent"}
```

Run API posting:

```powershell
py -3.14 run_operational_agent.py --date 2027-05-25 --post-api --no-dry-run
```

Run both SMTP and API delivery:

```powershell
py -3.14 run_operational_agent.py --date 2027-05-25 --send-email --post-api --no-dry-run
```

## Output files

```text
outbox/operational_delivery.jsonl
audit_logs/operational_agent_audit.jsonl
```

These files are local runtime outputs and should not be committed.

## Payload shape sent to API

```json
{
  "run_id": "uuid",
  "created_at_utc": "timestamp",
  "event": {
    "employee_id": "21001",
    "preferred_name": "Logan McNeil",
    "event_type": "birthday",
    "event_date": "2027-05-25",
    "days_until": 0,
    "department": "Human Resources",
    "email": "user@workday.net"
  },
  "message": "Generated celebration message",
  "delivery_recommendation": {
    "default_channel": "Email",
    "email_recipient": "user@workday.net",
    "manager_email": "manager@example.com"
  }
}
```

## Recommended demo flow

1. Open `app_operational.py`.
2. Click **Test Workday Connection**.
3. Set a business date that matches a birthday/anniversary.
4. Click **Preview Upcoming**.
5. Run in dry-run mode.
6. Verify outbox and audit logs.
7. Enable `SMTP_TO_OVERRIDE` and test SMTP.
8. Configure API endpoint and test API posting.
9. Remove test override only after approval.
