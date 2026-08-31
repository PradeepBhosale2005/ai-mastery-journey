# Final Demo Script - Employee Moments Assistant

Use this script for the final project walkthrough.

## Opening Statement

Hi, this is my AI Employee Birthday and Work Anniversary Celebration Agent. I have branded the user-facing experience as Employee Moments Assistant because the target users are HR teams, not technical users.

The goal is to reduce manual effort in tracking employee birthdays and work anniversaries, while keeping HR in control of review and sending.

## Problem Statement

HR teams often need to track employee celebrations manually. This can lead to missed birthdays, missed work anniversaries, inconsistent messages, and repetitive operational work.

## Solution Overview

This assistant connects with a Workday RaaS report, reads active employee celebration data, identifies birthdays and anniversaries, generates warm messages, and prepares them for HR review.

## Demo Flow

### 1. Show Workday Data Integration

Explain that the agent reads from the Workday RaaS report:

```text
RPT_AI_Employee_Celebration_Agent
```

Important fields used:

```text
Employee_ID
Preferred_Name
Email_-_Primary_Work_or_Primary_Home
CF-LRV-Manager_Email_Id
Active
Date_of_Workers_Next_Birthday
Original_Hire_Date
Supervisory_Organization
Time_Zone_of_Location_of_Worker_s_Primary_Position
```

### 2. Open HR-Friendly UI

Run:

```powershell
py -3.14 -m streamlit run app_hr.py
```

Show the dashboard named Employee Moments Assistant.

### 3. Show Summary Cards

Explain these cards:

- People Reviewed: active employees read from Workday
- Today: messages ready for review today
- Birthdays: upcoming birthday count
- Anniversaries: upcoming work anniversary count

### 4. Show Today's Celebrations

Open the Today tab. Explain that HR can see celebrations due today and preview each message before delivery.

### 5. Show Upcoming Celebrations

Open the Upcoming tab. Explain that HR can plan ahead and download the upcoming celebration list as CSV.

### 6. Show Message Preview

Open Message Preview. Select one employee and show the generated wish.

Mention that this can run in mock mode for demo or use a company LLM later through `.env` configuration.

### 7. Show Send Center

Open Send Center. Explain:

- Preview only mode is enabled by default.
- SMTP email and API posting are supported.
- Real sending is intentionally disabled for submission safety.
- HR should approve recipients and message tone before real sending.

### 8. Show Auditability

Explain that the agent writes delivery and audit records locally:

```text
outbox/
audit_logs/
```

These generated files are not committed because they may contain real employee output.

## Closing Statement

This project demonstrates a practical HR automation use case using Workday data, AI message generation, safe review controls, and a delivery-ready architecture. The project is built to be demo-safe now and production-extendable later through SMTP, APIs, or HR platform integrations.
