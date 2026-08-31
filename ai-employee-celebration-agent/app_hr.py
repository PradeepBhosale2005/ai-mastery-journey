from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from run_operational_agent import run_operational_agent
from src.actual_report_client import ActualWorkdayReportClient
from src.message_generator import CelebrationMessageGenerator
from src.upcoming_service import PlannedCelebration, find_planned_celebrations, planned_to_table


load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="Employee Moments Assistant",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.block-container {padding-top: 1.2rem; max-width: 1280px;}
.hr-hero {
  background: linear-gradient(135deg, #fff7ed 0%, #f0f9ff 52%, #f8fafc 100%);
  border: 1px solid #e8edf5;
  border-radius: 26px;
  padding: 28px 32px;
  margin-bottom: 18px;
}
.hr-title {font-size: 2.15rem; font-weight: 800; color: #172033; margin-bottom: 6px;}
.hr-subtitle {font-size: 1.05rem; color: #536179; max-width: 900px; line-height: 1.55;}
.card {
  background: #ffffff;
  border: 1px solid #e7ecf3;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 28px rgba(16, 24, 40, 0.05);
  min-height: 125px;
}
.card-title {font-size: .88rem; color: #667085; font-weight: 700; text-transform: uppercase; letter-spacing: .04em;}
.card-number {font-size: 2.2rem; font-weight: 800; color: #172033; margin-top: 6px;}
.card-note {font-size: .92rem; color: #6b7280; margin-top: 4px;}
.person-card {
  border: 1px solid #e8edf5;
  border-radius: 20px;
  padding: 18px;
  background: #ffffff;
  margin-bottom: 12px;
}
.person-name {font-size: 1.1rem; font-weight: 800; color: #172033; margin-bottom: 4px;}
.pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: #eef6ff;
  color: #175cd3;
  font-size: .82rem;
  font-weight: 700;
  margin-right: 6px;
}
.pill-today {background: #ecfdf3; color: #027a48;}
.pill-warn {background: #fff7ed; color: #b54708;}
.safe-box {
  background: #f8fafc;
  border: 1px solid #e7ecf3;
  border-radius: 18px;
  padding: 16px 18px;
  color: #344054;
}
.footer-note {font-size: .88rem; color: #667085;}
hr {margin-top: 1rem; margin-bottom: 1rem;}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner=False)
def load_workday_people() -> list:
    client = ActualWorkdayReportClient.from_env()
    return client.get_all_employees()


def build_planned(run_date: date, lookahead_days: int) -> tuple[list, list[PlannedCelebration]]:
    employees = load_workday_people()
    active_people = [employee for employee in employees if employee.is_active]
    planned = find_planned_celebrations(active_people, run_date, lookahead_days=lookahead_days)
    return employees, planned


def friendly_event_name(event_type: str) -> str:
    return "Birthday" if event_type == "birthday" else "Work Anniversary"


def generate_preview_message(planned: PlannedCelebration) -> str:
    return CelebrationMessageGenerator.from_env().generate(planned.event)


def config_label(value: bool) -> str:
    return "Ready" if value else "Not set"


def show_person_card(item: PlannedCelebration, allow_message_preview: bool = True) -> None:
    event = item.event
    employee = event.employee
    event_label = friendly_event_name(event.event_type)
    years_text = f" · {event.years} years" if event.years else ""
    today_class = "pill pill-today" if item.is_today else "pill"

    st.markdown(
        f"""
<div class="person-card">
  <div class="person-name">{employee.preferred_name}</div>
  <span class="{today_class}">{item.priority_label}</span>
  <span class="pill">{event_label}{years_text}</span>
  <span class="pill">{item.event_date.isoformat()}</span>
  <p style="margin-top: 12px; margin-bottom: 2px; color:#536179;">
    {employee.department or 'Department not available'} · {employee.country or 'Country not available'}
  </p>
  <p style="margin-top: 0; color:#667085; font-size:.92rem;">
    Email: {employee.email or 'Not available'} | Manager: {employee.manager_email or 'Not available'}
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    if allow_message_preview:
        with st.expander(f"Preview message for {employee.preferred_name}"):
            st.write(generate_preview_message(item))


def render_summary_cards(employees: list, planned: list[PlannedCelebration]) -> None:
    active_count = sum(1 for employee in employees if employee.is_active)
    due_today = [item for item in planned if item.is_today]
    birthdays = [item for item in planned if item.event.event_type == "birthday"]
    anniversaries = [item for item in planned if item.event.event_type == "work_anniversary"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><div class='card-title'>People Reviewed</div><div class='card-number'>{active_count}</div><div class='card-note'>Active employees from Workday</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><div class='card-title'>Today</div><div class='card-number'>{len(due_today)}</div><div class='card-note'>Messages ready to review</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><div class='card-title'>Birthdays</div><div class='card-number'>{len(birthdays)}</div><div class='card-note'>Within selected window</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><div class='card-title'>Anniversaries</div><div class='card-number'>{len(anniversaries)}</div><div class='card-note'>Within selected window</div></div>", unsafe_allow_html=True)


def run_delivery(run_date: date, lookahead_days: int, send_email: bool, post_api: bool, include_upcoming: bool, dry_run: bool) -> dict:
    return run_operational_agent(
        run_date=run_date,
        lookahead_days=lookahead_days,
        notify_upcoming=include_upcoming,
        send_email=send_email,
        post_api=post_api,
        dry_run=dry_run,
    )


st.markdown(
    """
<div class="hr-hero">
  <div class="hr-title">Employee Moments Assistant</div>
  <div class="hr-subtitle">
    Review upcoming birthdays and work anniversaries, preview warm AI-generated wishes,
    and send approved messages through email or another HR platform. Built for HR review first,
    not automatic blind sending.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Celebration Settings")
    selected_date = st.date_input("Review date", value=date.today(), help="The date HR wants to review or send messages for.")
    lookahead_days = st.slider("Show upcoming celebrations", 7, 120, 30, help="How far ahead HR wants to preview birthdays and anniversaries.")

    st.divider()
    st.header("Send Options")
    dry_run = st.toggle("Preview only", value=True, help="Recommended. Nothing is actually sent while this is on.")
    send_email = st.checkbox("Send by email", value=False)
    post_api = st.checkbox("Post to another HR app/API", value=False)
    include_upcoming = st.checkbox("Also send upcoming items", value=False, help="By default only today's celebrations are sent.")

    st.divider()
    refresh = st.button("Refresh Workday data", use_container_width=True)
    run_button = st.button("Review & Send", type="primary", use_container_width=True)

if refresh:
    load_workday_people.clear()

try:
    employees, planned = build_planned(selected_date, lookahead_days)
except Exception as exc:
    st.error("I could not read the Workday celebration report.")
    st.info("Check that your .env file has the Workday report URL and credentials, then try Refresh Workday data.")
    st.code(str(exc))
    st.stop()

render_summary_cards(employees, planned)

st.write("")
main_tab, today_tab, upcoming_tab, message_tab, send_tab, setup_tab = st.tabs(
    ["Overview", "Today", "Upcoming", "Message Preview", "Send Center", "Setup Help"]
)

with main_tab:
    st.subheader("What HR should look at first")
    due_today = [item for item in planned if item.is_today]
    if due_today:
        st.success(f"{len(due_today)} celebration item(s) are due today. Review the messages before sending.")
    else:
        st.info("No celebration messages are due today. You can still review upcoming items.")

    st.markdown(
        """
<div class="safe-box">
<b>Recommended HR process</b><br>
1. Review today's celebrations.<br>
2. Open message previews and adjust tone if needed.<br>
3. Keep Preview only on until the recipient list is confirmed.<br>
4. Send by email or post to your HR platform only after approval.
</div>
""",
        unsafe_allow_html=True,
    )

with today_tab:
    st.subheader("Celebrations due today")
    today_items = [item for item in planned if item.is_today]
    if not today_items:
        st.info("No birthdays or work anniversaries are due today.")
    for item in today_items:
        show_person_card(item)

with upcoming_tab:
    st.subheader(f"Upcoming celebrations in the next {lookahead_days} days")
    if planned:
        rows = planned_to_table(planned)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.download_button(
            "Download upcoming list",
            data=pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
            file_name="upcoming_employee_celebrations.csv",
            mime="text/csv",
        )
    else:
        st.info("No upcoming birthdays or anniversaries found for the selected window.")

with message_tab:
    st.subheader("Message previews")
    st.caption("These are the messages HR can review before delivery.")
    if planned:
        selected_name = st.selectbox(
            "Choose employee",
            options=[f"{item.event.employee.preferred_name} - {friendly_event_name(item.event.event_type)} - {item.event_date.isoformat()}" for item in planned],
        )
        selected_index = [f"{item.event.employee.preferred_name} - {friendly_event_name(item.event.event_type)} - {item.event_date.isoformat()}" for item in planned].index(selected_name)
        selected_item = planned[selected_index]
        message = generate_preview_message(selected_item)
        st.text_area("Generated message", value=message, height=170)
        st.markdown("<p class='footer-note'>Current version previews messages. Manual edits in this box are for HR review only; delivery uses generated message.</p>", unsafe_allow_html=True)
    else:
        st.info("No messages to preview for the selected date range.")

with send_tab:
    st.subheader("Send Center")
    st.markdown(
        """
<div class="safe-box">
<b>Safety check before sending</b><br>
- Use Preview only for testing.<br>
- Use SMTP_TO_OVERRIDE for first email test so all messages go to your mailbox.<br>
- Turn off Preview only only after HR approves the recipient list and message tone.
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Preview only", "On" if dry_run else "Off")
    c2.metric("Email", "Selected" if send_email else "Not selected")
    c3.metric("API Post", "Selected" if post_api else "Not selected")

    if run_button:
        summary = run_delivery(selected_date, lookahead_days, send_email, post_api, include_upcoming, dry_run)
        st.success("Run completed.")
        st.json({
            "run_id": summary["run_id"],
            "due_today": summary["due_today_count"],
            "upcoming": summary["upcoming_count"],
            "delivery_items": summary["delivery_scope_count"],
            "preview_only": summary["dry_run"],
        })

        delivery_rows = []
        for delivery in summary["deliveries"]:
            event = delivery["event"]
            for result in delivery["delivery_results"]:
                delivery_rows.append(
                    {
                        "Employee": event["preferred_name"],
                        "Moment": friendly_event_name(event["event_type"]),
                        "Date": event["event_date"],
                        "Channel": result["channel"],
                        "Status": result["status"],
                        "Target": result["target"],
                    }
                )
        if delivery_rows:
            st.dataframe(pd.DataFrame(delivery_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No delivery items were created. By default, only today's items are delivered.")

with setup_tab:
    st.subheader("Plain-English setup checklist")
    smtp_ready = bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_FROM_EMAIL"))
    api_ready = bool(os.getenv("POST_TARGET_API_URL"))
    workday_ready = bool(os.getenv("WORKDAY_RAAS_URL"))

    setup_rows = [
        {"Area": "Workday report", "Status": config_label(workday_ready), "What HR needs": "The celebration report must be accessible."},
        {"Area": "Email sending", "Status": config_label(smtp_ready), "What HR needs": "SMTP details from IT or a mailbox app password."},
        {"Area": "Other HR app/API", "Status": config_label(api_ready), "What HR needs": "Webhook/API URL from the target platform."},
        {"Area": "AI message mode", "Status": os.getenv("LLM_PROVIDER", "mock"), "What HR needs": "Mock is safe for demo. Company LLM can be enabled later."},
    ]
    st.dataframe(pd.DataFrame(setup_rows), use_container_width=True, hide_index=True)

    st.markdown(
        """
### Email setup fields
Ask IT for these values, then add them to `.env`:

```text
SMTP_ENABLED=true
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=Employee Moments Assistant
SMTP_USE_TLS=true
SMTP_TO_OVERRIDE=your.test.email@company.com
```

Keep `SMTP_TO_OVERRIDE` filled during testing. Remove it only when HR is ready to send to real employees.
"""
    )
