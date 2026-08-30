from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.audit_logger import AuditLogger
from src.celebration_detector import CelebrationDetector
from src.message_generator import CelebrationMessageGenerator
from src.notification_service import NotificationService
from src.real_workday_client import RealWorkdayRaaSClient


def parse_run_date(value: str | date | datetime | None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def run_real_workday_celebration_agent(
    run_date: str | date | datetime | None = None,
    outbox_path: str | Path | None = None,
    audit_log_path: str | Path | None = None,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Run the celebration agent using a real Workday RaaS JSON endpoint."""
    load_dotenv()

    resolved_run_date = parse_run_date(run_date)
    resolved_outbox_path = outbox_path or os.getenv("DEFAULT_OUTBOX_PATH", "outbox/notifications.jsonl")
    resolved_audit_log_path = audit_log_path or os.getenv("DEFAULT_AUDIT_LOG_PATH", "audit_logs/agent_audit.jsonl")

    audit_logger = AuditLogger(resolved_audit_log_path)
    audit_logger.log(
        "REAL_WORKDAY_RUN_STARTED",
        {
            "run_date": resolved_run_date.isoformat(),
            "dry_run": dry_run,
            "workday_raas_url_configured": bool(os.getenv("WORKDAY_RAAS_URL") or os.getenv("WORKDAY_RAS_URL")),
        },
    )

    workday_client = RealWorkdayRaaSClient.from_env()
    employees = workday_client.get_all_employees()
    active_employees = [employee for employee in employees if employee.is_active]

    detector = CelebrationDetector()
    events = detector.find_events(active_employees, resolved_run_date)

    audit_logger.log(
        "REAL_WORKDAY_EVENTS_DETECTED",
        {
            "employee_count": len(employees),
            "active_employee_count": len(active_employees),
            "events_found": len(events),
            "events": [event.to_dict() for event in events],
        },
    )

    message_generator = CelebrationMessageGenerator.from_env()
    notification_service = NotificationService(resolved_outbox_path, dry_run=dry_run)

    notifications = []
    for event in events:
        message = message_generator.generate(event)
        result = notification_service.send(event, message)
        notifications.append(result.to_dict())
        audit_logger.log(
            "REAL_WORKDAY_NOTIFICATION_PREPARED",
            {
                "event": event.to_dict(),
                "notification": result.to_dict(),
            },
        )

    summary = {
        "use_case_name": "AI Employee Birthday & Work Anniversary Celebration Agent",
        "data_source": "Real Workday RaaS API",
        "run_date": resolved_run_date.isoformat(),
        "employees_scanned": len(employees),
        "active_employees_scanned": len(active_employees),
        "events_found": len(events),
        "notifications_prepared": len(notifications),
        "events": [event.to_dict() for event in events],
        "notifications": notifications,
        "dry_run": dry_run,
    }
    audit_logger.log("REAL_WORKDAY_RUN_COMPLETED", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Employee Celebration Agent with real Workday RaaS data")
    parser.add_argument("--date", default=None, help="Run date in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--outbox", default="outbox/real_workday_notifications.jsonl", help="Notification outbox JSONL path.")
    parser.add_argument("--audit", default="audit_logs/real_workday_agent_audit.jsonl", help="Audit log JSONL path.")
    parser.add_argument("--send", action="store_true", help="Use simulated sent status instead of dry-run status.")
    args = parser.parse_args()

    summary = run_real_workday_celebration_agent(
        run_date=args.date,
        outbox_path=args.outbox,
        audit_log_path=args.audit,
        dry_run=not args.send,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
