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
from src.upcoming_service import find_planned_celebrations, planned_to_table


load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(page_title="AI Celebration Agent", page_icon="🎉", layout="wide")

st.markdown(
    """
<style>
.block-container {padding-top: 1.3rem;}
.metric-card {border: 1px solid #e7e7e7; border-radius: 14px; padding: 18px; background: #fbfbfd;}
.status-ok {color: #087443; font-weight: 700;}
.status-warn {color: #a15c00; font-weight: 700;}
.status-bad {color: #b42318; font-weight: 700;}
.small-note {font-size: 0.9rem; color: #667085;}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🎉 AI Employee Celebration Agent")
st.caption("Workday RaaS + upcoming birthday/anniversary planning + SMTP/API delivery + audit trail")

with st.sidebar:
    st.header("Run Controls")
    run_date = st.date_input("Business date", value=date.today())
    lookahead_days = st.slider("Upcoming window", min_value=1, max_value=120, value=30)
    notify_upcoming = st.checkbox("Deliver upcoming events too", value=False)

    st.divider()
    st.subheader("Delivery")
    dry_run = st.checkbox("Dry run", value=True, help="Keep enabled until SMTP/API configuration is tested.")
    send_email = st.checkbox("Use SMTP email", value=False)
    post_api = st.checkbox("Post to generic API", value=False)

    if not dry_run and (send_email or post_api):
        st.warning("Real delivery is enabled. Confirm recipients and API target before running.")

    test_button = st.button("Test Workday Connection")
    preview_button = st.button("Preview Upcoming")
    run_button = st.button("Run Agent", type="primary")


def config_status() -> list[dict[str, str]]:
    return [
        {"Config": "Workday RaaS URL", "Status": "Configured" if os.getenv("WORKDAY_RAAS_URL") else "Missing"},
        {"Config": "Workday Auth", "Status": "Configured" if (os.getenv("WORKDAY_ACCESS_TOKEN") or os.getenv("WORKDAY_USERNAME")) else "Missing"},
        {"Config": "LLM Provider", "Status": os.getenv("LLM_PROVIDER", "mock")},
        {"Config": "SMTP", "Status": "Enabled" if os.getenv("SMTP_ENABLED", "false").lower() == "true" else "Disabled"},
        {"Config": "Generic API", "Status": "Enabled" if os.getenv("POST_TARGET_API_ENABLED", "false").lower() == "true" else "Disabled"},
    ]


def load_employees():
    client = ActualWorkdayReportClient.from_env()
    return client.get_all_employees()


def render_metrics(summary: dict):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Employees", summary["employees_scanned"])
    col2.metric("Active", summary["active_employees_scanned"])
    col3.metric("Due Today", summary["due_today_count"])
    col4.metric("Upcoming", summary["upcoming_count"])
    col5.metric("Delivery Items", summary["delivery_scope_count"])


tab_dashboard, tab_upcoming, tab_delivery, tab_setup = st.tabs(["Dashboard", "Upcoming", "Delivery Results", "Setup"])

with tab_setup:
    st.subheader("Configuration Status")
    st.dataframe(pd.DataFrame(config_status()), use_container_width=True, hide_index=True)
    st.markdown(
        """
**Safety rules**

- `.env` stays local and must not be committed.
- Keep **Dry run** enabled until Workday, SMTP, and API settings are verified.
- Use `SMTP_TO_OVERRIDE` during testing so emails go only to your test mailbox.
- Use generic API posting for systems such as Teams webhook, HR tools, internal apps, or a custom middleware endpoint.
"""
    )

if test_button:
    with tab_dashboard:
        try:
            employees = load_employees()
            active_count = sum(1 for employee in employees if employee.is_active)
            st.success(f"Connected successfully. Employees fetched: {len(employees)} | Active: {active_count}")
            st.dataframe(pd.DataFrame([employee.preview_dict() for employee in employees[:10]]), use_container_width=True, hide_index=True)
        except Exception as exc:
            st.error(f"Connection test failed: {exc}")

if preview_button:
    with tab_upcoming:
        try:
            employees = load_employees()
            active = [employee for employee in employees if employee.is_active]
            planned = find_planned_celebrations(active, run_date, lookahead_days=lookahead_days)
            rows = planned_to_table(planned)
            st.success(f"Found {len(rows)} planned celebrations in the next {lookahead_days} days.")
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            else:
                st.info("No upcoming celebrations found for this window.")
        except Exception as exc:
            st.error(f"Preview failed: {exc}")

if run_button:
    try:
        summary = run_operational_agent(
            run_date=run_date,
            lookahead_days=lookahead_days,
            notify_upcoming=notify_upcoming,
            send_email=send_email,
            post_api=post_api,
            dry_run=dry_run,
        )

        with tab_dashboard:
            st.success("Agent run completed.")
            render_metrics(summary)
            st.json({key: summary[key] for key in ["run_id", "run_date", "dry_run", "send_email", "post_api", "notify_upcoming"]})

        with tab_upcoming:
            if summary["upcoming"]:
                st.dataframe(pd.DataFrame(summary["upcoming"]), use_container_width=True, hide_index=True)
            else:
                st.info("No upcoming celebrations found.")

        with tab_delivery:
            delivery_rows = []
            for item in summary["deliveries"]:
                event = item["event"]
                for result in item["delivery_results"]:
                    delivery_rows.append(
                        {
                            "Name": event["preferred_name"],
                            "Event": event["event_type"],
                            "Event Date": event["event_date"],
                            "Channel": result["channel"],
                            "Status": result["status"],
                            "Target": result["target"],
                            "Detail": result["detail"],
                        }
                    )
            if delivery_rows:
                st.dataframe(pd.DataFrame(delivery_rows), use_container_width=True, hide_index=True)
                for item in summary["deliveries"]:
                    event = item["event"]
                    with st.expander(f"{event['preferred_name']} - {event['event_type']} message"):
                        st.write(item["message"])
            else:
                st.info("No deliveries were generated. By default, only due-today events are delivered.")
    except Exception as exc:
        st.error(f"Agent run failed: {exc}")
else:
    with tab_dashboard:
        st.info("Use the sidebar to test Workday, preview upcoming celebrations, or run the agent.")
        st.dataframe(pd.DataFrame(config_status()), use_container_width=True, hide_index=True)
