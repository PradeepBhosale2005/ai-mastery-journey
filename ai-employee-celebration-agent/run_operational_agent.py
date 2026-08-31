from __future__ import annotations

import argparse
import json
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.actual_report_client import ActualWorkdayReportClient
from src.audit_logger import AuditLogger
from src.delivery_service import OperationalDeliveryService
from src.message_generator import CelebrationMessageGenerator
from src.upcoming_service import find_planned_celebrations, planned_to_table


def parse_run_date(value: str | date | datetime | None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def run_operational_agent(
    run_date: str | date | datetime | None = None,
    lookahead_days: int = 30,
    notify_upcoming: bool = False,
    send_email: bool = False,
    post_api: bool = False,
    dry_run: bool = True,
    outbox_path: str | Path = "outbox/operational_delivery.jsonl",
    audit_log_path: str | Path = "audit_logs/operational_agent_audit.jsonl",
) -> dict[str, Any]:
    """Run the production-style celebration agent.

    The agent always previews upcoming events. It sends/delivers only today's
    events unless notify_upcoming=True.
    """
    load_dotenv()
    run_id = str(uuid.uuid4())
    business_date = parse_run_date(run_date)

    audit_logger = AuditLogger(audit_log_path)
    audit_logger.log(
        "OPERATIONAL_RUN_STARTED",
        {
            "run_id": run_id,
            "run_date": business_date.isoformat(),
            "lookahead_days": lookahead_days,
            "notify_upcoming": notify_upcoming,
            "send_email": send_email,
            "post_api": post_api,
            "dry_run": dry_run,
        },
    )

    client = ActualWorkdayReportClient.from_env()
    employees = client.get_all_employees()
    active_employees = [employee for employee in employees if employee.is_active]
    planned = find_planned_celebrations(active_employees, business_date, lookahead_days=lookahead_days)

    due_today = [item for item in planned if item.is_today]
    delivery_scope = planned if notify_upcoming else due_today

    message_generator = CelebrationMessageGenerator.from_env()
    delivery_service = OperationalDeliveryService(outbox_path=outbox_path)

    deliveries = []
    for item in delivery_scope:
        message = message_generator.generate(item.event)
        result = delivery_service.deliver(
            planned=item,
            message=message,
            run_id=run_id,
            dry_run=dry_run,
            send_email=send_email,
            post_api=post_api,
        )
        deliveries.append(
            {
                "event": item.to_dict(),
                "message": message,
                "delivery_results": result,
            }
        )

    summary = {
        "run_id": run_id,
        "use_case_name": "AI Employee Birthday & Work Anniversary Celebration Agent",
        "data_source": "RPT_AI_Employee_Celebration_Agent Workday RaaS Report",
        "run_date": business_date.isoformat(),
        "lookahead_days": lookahead_days,
        "employees_scanned": len(employees),
        "active_employees_scanned": len(active_employees),
        "due_today_count": len(due_today),
        "upcoming_count": len(planned),
        "delivery_scope_count": len(delivery_scope),
        "delivery_results_count": sum(len(item["delivery_results"]) for item in deliveries),
        "dry_run": dry_run,
        "send_email": send_email,
        "post_api": post_api,
        "notify_upcoming": notify_upcoming,
        "upcoming": planned_to_table(planned),
        "deliveries": deliveries,
    }
    audit_logger.log("OPERATIONAL_RUN_COMPLETED", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run operational celebration agent with Workday, SMTP, and API delivery")
    parser.add_argument("--date", default=None, help="Business date in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--lookahead-days", type=int, default=30, help="Upcoming celebration window.")
    parser.add_argument("--notify-upcoming", action="store_true", help="Deliver upcoming events too. Default delivers only due-today events.")
    parser.add_argument("--send-email", action="store_true", help="Attempt real SMTP delivery when dry-run is disabled.")
    parser.add_argument("--post-api", action="store_true", help="Attempt real generic API POST when dry-run is disabled.")
    parser.add_argument("--no-dry-run", action="store_true", help="Actually send enabled delivery channels. Use carefully.")
    parser.add_argument("--outbox", default="outbox/operational_delivery.jsonl")
    parser.add_argument("--audit", default="audit_logs/operational_agent_audit.jsonl")
    args = parser.parse_args()

    summary = run_operational_agent(
        run_date=args.date,
        lookahead_days=args.lookahead_days,
        notify_upcoming=args.notify_upcoming,
        send_email=args.send_email,
        post_api=args.post_api,
        dry_run=not args.no_dry_run,
        outbox_path=args.outbox,
        audit_log_path=args.audit,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
