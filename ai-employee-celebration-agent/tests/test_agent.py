import json
from pathlib import Path

from src.agent import run_celebration_agent


def test_agent_runs_with_sample_data(tmp_path: Path) -> None:
    sample_data = [
        {
            "employee_id": "E300",
            "worker_id": "W300",
            "preferred_name": "Demo User",
            "legal_name": "Demo User",
            "email": "demo.user@example.com",
            "manager_email": "manager@example.com",
            "date_of_birth": "1995-08-29",
            "hire_date": "2020-08-29",
            "timezone": "Asia/Kolkata",
            "country": "India",
            "department": "Engineering",
            "status": "Active",
            "celebration_channel": "Email",
        }
    ]
    data_path = tmp_path / "employees.json"
    outbox_path = tmp_path / "outbox.jsonl"
    audit_path = tmp_path / "audit.jsonl"
    data_path.write_text(json.dumps(sample_data), encoding="utf-8")

    summary = run_celebration_agent(
        run_date="2026-08-29",
        data_path=data_path,
        outbox_path=outbox_path,
        audit_log_path=audit_path,
        dry_run=True,
    )

    assert summary["events_found"] == 2
    assert summary["notifications_prepared"] == 2
    assert outbox_path.exists()
    assert audit_path.exists()
