from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.agent import run_celebration_agent


st.set_page_config(page_title="AI Employee Celebration Agent", page_icon="🎉", layout="wide")

st.title("AI Employee Birthday & Work Anniversary Celebration Agent")
st.caption("Mock Workday API + AI message generation + notification simulation")

with st.sidebar:
    st.header("Run Settings")
    run_date = st.date_input("Business date", value=date(2026, 8, 29))
    data_path = st.text_input("Mock Workday data", value="data/mock_workday_employees.json")
    dry_run = st.checkbox("Dry run", value=True)
    run_button = st.button("Run Agent", type="primary")

st.markdown(
    """
This MVP scans active employees, checks birthdays and work anniversaries against the selected business date,
generates a personalized message, and records simulated notifications for Email or Jadean Jar.
"""
)

if run_button:
    summary = run_celebration_agent(run_date=run_date, data_path=data_path, dry_run=dry_run)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Employees Scanned", summary["employees_scanned"])
    col2.metric("Active Employees", summary["active_employees_scanned"])
    col3.metric("Events Found", summary["events_found"])
    col4.metric("Notifications", summary["notifications_prepared"])

    st.subheader("Detected Celebrations")
    if summary["events"]:
        st.dataframe(pd.DataFrame(summary["events"]), use_container_width=True)
    else:
        st.info("No celebrations found for the selected date.")

    st.subheader("Prepared Notifications")
    if summary["notifications"]:
        st.dataframe(pd.DataFrame(summary["notifications"]), use_container_width=True)
        for notification in summary["notifications"]:
            with st.expander(f"{notification['event_type']} - {notification['recipient']}"):
                st.write(notification["message"])
    else:
        st.info("No notifications prepared.")

    st.subheader("Raw Agent Output")
    st.json(summary)
else:
    st.info("Click Run Agent to execute the demo workflow.")
