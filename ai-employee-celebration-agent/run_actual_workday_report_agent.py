from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.actual_report_client import ActualReportEmployee, ActualWorkdayReportClient
from src.audit_logger import AuditLogger
from src.message_generator import CelebrationMessageGenerator
from src.models import CelebrationEvent, Employee
from src.notification_service import NotificationService


def parse_run_date(value: str | date | datetime | None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def find_events_from_actual_report(
    employees: list[ActualReportEmployee],
    run_date: date,
) -> list[CelebrationEvent]:
    """Detect events from the exact RPT_AI_Employee_Celebration_Agent report.

    Birthday detection uses Date_of_Workers_Next_Birthday as an exact date match.
    Anniversary detection uses Original_Hire_Date month/day and calculates years.
    """
    events: list[CelebrationEvent] = []

    for report_employee in employees:
        if not report_employee.is_active:
            continue

        event_employee = Employee.from_dict(report_employee.to_event_employee_dict())

        if report_employee.next_birthday_date == run_date:
            events.append(
                CelebrationEvent(
                    employee=event_employee,
                    event_type="birthday",
                    celebration_date=report_employee.next_birthday_date,
                    years=None,
                    local_date=run_date,
                    source_system="Workday RaaS Report",
                )
            )

        if report_employee.original_hire_date and _same_month_day(report_employee.original_hire_date, run_date):
            anniversary_years = _years_since(report_employee.original_hire_date, run_date)
            if anniversary_years > 0:
                events.append(
                    CelebrationEvent(
                        employee=event_employee,
                        event_type="work_anniversary",
                        celebration_date=report_employee.original_hire_date,
                        years=anniversary_years,
                        local_date=run_date,
                        source_system="Workday RaaS Report",
                    )
                )

    return events


def run_actual_workday_report_agent(
    run_date: str | date | datetime | None = None,
    outbox_path: str | Path = "outbox/actual_workday_report_notifications.jsonl",
    audit_log_path: str | Path = "audit_logs/actual_workday_report_agent_audit.jsonl",
    dry_run: bool = True,
) -> dict[str, Any]:
    load_dotenv()
    resolved_run_date = parse_run_date(run_date)

    audit_logger = AuditLogger(audit_log_path)
    audit_logger.log("ACTUAL_REPORT_RUN_STARTED", {"run_date": resolved_run_date.isoformat(), "dry_run": dry_run})

    client = ActualWorkdayReportClient.from_env()
    employees = client.get_all_employees()
    active_employees = [employee for employee in employees if employee.is_active]
    events = find_events_from_actual_report(active_employees, resolved_run_date)

    message_generator = CelebrationMessageGenerator.from_env()
    notification_service = NotificationService(outbox_path, dry_run=dry_run)

    notifications = []
    for event in events:
        message = message_generator.generate(event)
        result = notification_service.send(event, message)
        notifications.append(result.to_dict())
        audit_logger.log(
            "ACTUAL_REPORT_NOTIFICATION_PREPARED",
            {"event": event.to_dict(), "notification": result.to_dict()},
        )

    summary = {
        "use_case_name": "AI Employee Birthday & Work Anniversary Celebration Agent",
        "data_source": "RPT_AI_Employee_Celebration_Agent Workday RaaS Report",
        "run_date": resolved_run_date.isoformat(),
        "employees_scanned": len(employees),
        "active_employees_scanned": len(active_employees),
        "events_found": len(events),
        "notifications_prepared": len(notifications),
        "events": [event.to_dict() for event in events],
        "notifications": notifications,
        "dry_run": dry_run,
    }
    audit_logger.log("ACTUAL_REPORT_RUN_COMPLETED", summary)
    return summary


def _same_month_day(value: date, target_date: date) -> bool:
    return value.month == target_date.month and value.day == target_date.day


def _years_since(start_date: date, target_date: date) -> int:
    years = target_date.year - start_date.year
    if (target_date.month, target_date.day) < (start_date.month, start_date.day):
        years -= 1
    return years


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the celebration agent using the exact Workday RaaS report")
    parser.add_argument("--date", default=None, help="Business date in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--outbox", default="outbox/actual_workday_report_notifications.jsonl")
    parser.add_argument("--audit", default="audit_logs/actual_workday_report_agent_audit.jsonl")
    parser.add_argument("--send", action="store_true", help="Use simulated sent status instead of dry-run status.")
    args = parser.parse_args()

    summary = run_actual_workday_report_agent(
        run_date=args.date,
        outbox_path=args.outbox,
        audit_log_path=args.audit,
        dry_run=not args.send,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
