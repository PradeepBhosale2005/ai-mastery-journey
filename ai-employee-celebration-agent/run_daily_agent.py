from __future__ import annotations

import argparse
import json

from src.agent import run_celebration_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Employee Celebration Agent")
    parser.add_argument("--date", default=None, help="Run date in YYYY-MM-DD format. Defaults to today.")
    parser.add_argument("--data", default="data/mock_workday_employees.json", help="Path to mock Workday employee JSON.")
    parser.add_argument("--outbox", default="outbox/notifications.jsonl", help="Notification outbox JSONL path.")
    parser.add_argument("--audit", default="audit_logs/agent_audit.jsonl", help="Audit log JSONL path.")
    parser.add_argument("--send", action="store_true", help="Use simulated sent status instead of dry-run status.")
    args = parser.parse_args()

    summary = run_celebration_agent(
        run_date=args.date,
        data_path=args.data,
        outbox_path=args.outbox,
        audit_log_path=args.audit,
        dry_run=not args.send,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
