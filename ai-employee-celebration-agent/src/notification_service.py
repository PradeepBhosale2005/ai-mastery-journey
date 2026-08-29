from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.models import CelebrationEvent, NotificationResult


class NotificationService:
    """Simulate email or Jadean Jar notifications and write them to an outbox."""

    def __init__(self, outbox_path: str | Path = "outbox/notifications.jsonl", dry_run: bool = True) -> None:
        self.outbox_path = Path(outbox_path)
        self.dry_run = dry_run

    def send(self, event: CelebrationEvent, message: str) -> NotificationResult:
        channel = event.employee.celebration_channel or "Email"
        recipient = event.employee.email if channel.lower() == "email" else "Jadean Jar Feed"
        status = "DRY_RUN_RECORDED" if self.dry_run else "SIMULATED_SENT"

        result = NotificationResult(
            employee_id=event.employee.employee_id,
            event_type=event.event_type,
            channel=channel,
            recipient=recipient,
            message=message,
            status=status,
            simulated=True,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
        self._write_outbox(result)
        return result

    def _write_outbox(self, result: NotificationResult) -> None:
        self.outbox_path.parent.mkdir(parents=True, exist_ok=True)
        with self.outbox_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")
