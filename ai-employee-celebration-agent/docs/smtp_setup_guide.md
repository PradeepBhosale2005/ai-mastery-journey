# SMTP Setup Guide for Employee Moments Assistant

This guide explains how HR or IT can enable email delivery for the AI Employee Birthday & Work Anniversary Celebration Agent.

## What SMTP Means

SMTP is the email sending service used by a mailbox or email server. In this project, SMTP lets the agent send birthday and work anniversary emails after HR review.

## Recommended Safe Rollout

1. Keep `Preview only` enabled in the UI.
2. Configure SMTP using a test mailbox first.
3. Set `SMTP_TO_OVERRIDE` to your own email address so every test email comes only to you.
4. Run a test for one known celebration date.
5. Ask HR/IT to approve the message tone and recipients.
6. Remove `SMTP_TO_OVERRIDE` only when real sending is approved.
7. Turn off `Preview only` only for approved sends.

## Required .env Values

Add these values to your local `.env` file only. Do not commit `.env`.

```text
SMTP_ENABLED=true
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=Employee Moments Assistant
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TO_OVERRIDE=your.test.email@company.com
SMTP_CC_LIST=
SMTP_CC_MANAGER=false
```

## Field Meaning

| Field | Meaning |
|---|---|
| SMTP_ENABLED | Must be true to allow SMTP sending. |
| SMTP_HOST | Your mail server address. Example: smtp.office365.com or smtp.gmail.com. |
| SMTP_PORT | Usually 587 for TLS. Sometimes 465 for SSL. |
| SMTP_USERNAME | Mailbox username. Usually the sender email address. |
| SMTP_PASSWORD | Mailbox password or app password. |
| SMTP_FROM_EMAIL | Email address shown as sender. |
| SMTP_FROM_NAME | Friendly sender name shown in email. |
| SMTP_USE_TLS | Usually true for port 587. |
| SMTP_USE_SSL | Usually true only for port 465. |
| SMTP_TO_OVERRIDE | Safety field. Sends all test emails to one mailbox. |
| SMTP_CC_LIST | Optional comma-separated CC recipients. |
| SMTP_CC_MANAGER | true to CC the employee manager when manager email exists. |

## Common Provider Examples

### Microsoft 365 / Outlook SMTP

```text
SMTP_ENABLED=true
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=celebrations@yourcompany.com
SMTP_PASSWORD=<mailbox-password-or-approved-app-password>
SMTP_FROM_EMAIL=celebrations@yourcompany.com
SMTP_FROM_NAME=Employee Moments Assistant
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TO_OVERRIDE=your.test.email@yourcompany.com
```

### Gmail SMTP

```text
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.gmail.address@gmail.com
SMTP_PASSWORD=<gmail-app-password>
SMTP_FROM_EMAIL=your.gmail.address@gmail.com
SMTP_FROM_NAME=Employee Moments Assistant
SMTP_USE_TLS=true
SMTP_USE_SSL=false
SMTP_TO_OVERRIDE=your.test.email@yourcompany.com
```

## Test Commands

Run preview-only first. This records the email action but does not send the message.

```powershell
py -3.14 run_operational_agent.py --date 2027-05-25 --send-email
```

Run real SMTP sending only after SMTP settings and recipients are approved.

```powershell
py -3.14 run_operational_agent.py --date 2027-05-25 --send-email --no-dry-run
```

## HR Friendly UI

Run the HR-friendly dashboard:

```powershell
py -3.14 -m streamlit run app_hr.py
```

Use this flow:

1. Open Setup Help.
2. Confirm Workday report is ready.
3. Keep Preview only enabled.
4. Review Today and Upcoming tabs.
5. Review message previews.
6. Test email with SMTP_TO_OVERRIDE.
7. Send only after approval.

## Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| SMTP says disabled | SMTP_ENABLED is false | Set SMTP_ENABLED=true in `.env`. |
| Missing SMTP settings | Host/from email/password not set | Fill required fields. |
| Authentication failed | Wrong password or app password | Ask IT to confirm SMTP auth. |
| Emails go to real employees during testing | SMTP_TO_OVERRIDE is blank | Add your own email to SMTP_TO_OVERRIDE. |
| SSL/TLS error | Wrong port/security setting | Use port 587 with TLS or 465 with SSL. |

## Security Notes

- Never commit `.env`.
- Do not paste SMTP password into chat.
- Prefer a service mailbox such as `celebrations@company.com`.
- Use least privilege and HR-approved sender policies.
- Keep audit logs for delivery traceability.
