from __future__ import annotations

import json
import os
import smtplib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from src.upcoming_service import PlannedCelebration


@dataclass(frozen=True)
class DeliveryResult:
    channel: str
    status: str
    target: str
    detail: str
    timestamp_utc: str
    response_status_code: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SMTPSettings:
    enabled: bool
    host: str
    port: int
    username: str
    password: str
    from_email: str
    from_name: str
    use_tls: bool
    use_ssl: bool
    to_override: str
    cc_list: list[str]
    cc_manager: bool

    @classmethod
    def from_env(cls) -> "SMTPSettings":
        load_dotenv()
        return cls(
            enabled=_bool_env("SMTP_ENABLED", False),
            host=os.getenv("SMTP_HOST", ""),
            port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USERNAME", ""),
            password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("SMTP_FROM_EMAIL", ""),
            from_name=os.getenv("SMTP_FROM_NAME", "AI Celebration Agent"),
            use_tls=_bool_env("SMTP_USE_TLS", True),
            use_ssl=_bool_env("SMTP_USE_SSL", False),
            to_override=os.getenv("SMTP_TO_OVERRIDE", ""),
            cc_list=_csv_env("SMTP_CC_LIST"),
            cc_manager=_bool_env("SMTP_CC_MANAGER", False),
        )

    def validate(self) -> list[str]:
        missing = []
        if not self.host:
            missing.append("SMTP_HOST")
        if not self.from_email:
            missing.append("SMTP_FROM_EMAIL")
        if self.username and not self.password:
            missing.append("SMTP_PASSWORD")
        return missing


@dataclass(frozen=True)
class APIPostSettings:
    enabled: bool
    url: str
    method: str
    bearer_token: str
    headers: dict[str, str]
    timeout_seconds: int

    @classmethod
    def from_env(cls) -> "APIPostSettings":
        load_dotenv()
        return cls(
            enabled=_bool_env("POST_TARGET_API_ENABLED", False),
            url=os.getenv("POST_TARGET_API_URL", ""),
            method=os.getenv("POST_TARGET_API_METHOD", "POST").upper(),
            bearer_token=os.getenv("POST_TARGET_API_BEARER_TOKEN", ""),
            headers=_json_env("POST_TARGET_API_HEADERS_JSON", {}),
            timeout_seconds=int(os.getenv("POST_TARGET_API_TIMEOUT_SECONDS", "30")),
        )


class OperationalDeliveryService:
    """Deliver celebration messages to outbox, SMTP, and any generic HTTP API."""

    def __init__(
        self,
        outbox_path: str | Path = "outbox/operational_delivery.jsonl",
        smtp_settings: SMTPSettings | None = None,
        api_settings: APIPostSettings | None = None,
    ) -> None:
        self.outbox_path = Path(outbox_path)
        self.smtp_settings = smtp_settings or SMTPSettings.from_env()
        self.api_settings = api_settings or APIPostSettings.from_env()

    def deliver(
        self,
        planned: PlannedCelebration,
        message: str,
        run_id: str,
        dry_run: bool = True,
        send_email: bool = False,
        post_api: bool = False,
    ) -> list[dict[str, Any]]:
        payload = self._build_payload(planned, message, run_id)
        results = [self._write_outbox(payload).to_dict()]

        if send_email:
            results.append(self._send_smtp(planned, message, dry_run=dry_run).to_dict())

        if post_api:
            results.append(self._post_api(payload, dry_run=dry_run).to_dict())

        return results

    def _build_payload(self, planned: PlannedCelebration, message: str, run_id: str) -> dict[str, Any]:
        event = planned.event
        return {
            "run_id": run_id,
            "created_at_utc": _utc_now(),
            "event": planned.to_dict(),
            "message": message,
            "delivery_recommendation": {
                "default_channel": event.employee.celebration_channel,
                "email_recipient": event.employee.email,
                "manager_email": event.employee.manager_email,
            },
        }

    def _write_outbox(self, payload: dict[str, Any]) -> DeliveryResult:
        self.outbox_path.parent.mkdir(parents=True, exist_ok=True)
        with self.outbox_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return DeliveryResult(
            channel="jsonl_outbox",
            status="RECORDED",
            target=str(self.outbox_path),
            detail="Payload recorded in local JSONL outbox.",
            timestamp_utc=_utc_now(),
        )

    def _send_smtp(self, planned: PlannedCelebration, message: str, dry_run: bool) -> DeliveryResult:
        settings = self.smtp_settings
        employee = planned.event.employee
        recipient = settings.to_override or employee.email

        if dry_run:
            return DeliveryResult("smtp_email", "DRY_RUN", recipient, "SMTP send skipped because dry_run=True.", _utc_now())

        if not settings.enabled:
            return DeliveryResult("smtp_email", "SKIPPED_DISABLED", recipient, "SMTP_ENABLED is false.", _utc_now())

        missing = settings.validate()
        if missing:
            return DeliveryResult("smtp_email", "FAILED_CONFIG", recipient, f"Missing SMTP settings: {', '.join(missing)}", _utc_now())

        if not recipient:
            return DeliveryResult("smtp_email", "FAILED_NO_RECIPIENT", "", "No employee email or SMTP_TO_OVERRIDE configured.", _utc_now())

        email = EmailMessage()
        email["Subject"] = _subject_for(planned)
        email["From"] = f"{settings.from_name} <{settings.from_email}>"
        email["To"] = recipient
        cc_values = list(settings.cc_list)
        if settings.cc_manager and employee.manager_email:
            cc_values.append(employee.manager_email)
        if cc_values:
            email["Cc"] = ", ".join(sorted(set(cc_values)))
        email.set_content(_email_body(planned, message))

        try:
            if settings.use_ssl:
                with smtplib.SMTP_SSL(settings.host, settings.port, timeout=30) as server:
                    _smtp_login(server, settings)
                    server.send_message(email)
            else:
                with smtplib.SMTP(settings.host, settings.port, timeout=30) as server:
                    if settings.use_tls:
                        server.starttls()
                    _smtp_login(server, settings)
                    server.send_message(email)
            return DeliveryResult("smtp_email", "SENT", recipient, "Email sent through SMTP.", _utc_now())
        except Exception as exc:  # pragma: no cover - network path
            return DeliveryResult("smtp_email", "FAILED_SEND", recipient, str(exc), _utc_now())

    def _post_api(self, payload: dict[str, Any], dry_run: bool) -> DeliveryResult:
        settings = self.api_settings
        if dry_run:
            return DeliveryResult("generic_api", "DRY_RUN", settings.url, "API post skipped because dry_run=True.", _utc_now())

        if not settings.enabled:
            return DeliveryResult("generic_api", "SKIPPED_DISABLED", settings.url, "POST_TARGET_API_ENABLED is false.", _utc_now())

        if not settings.url:
            return DeliveryResult("generic_api", "FAILED_CONFIG", "", "POST_TARGET_API_URL is missing.", _utc_now())

        headers = {"Content-Type": "application/json", **settings.headers}
        if settings.bearer_token:
            headers["Authorization"] = f"Bearer {settings.bearer_token}"

        try:
            response = requests.request(
                settings.method,
                settings.url,
                headers=headers,
                json=payload,
                timeout=settings.timeout_seconds,
            )
            status = "POSTED" if 200 <= response.status_code < 300 else "FAILED_HTTP"
            return DeliveryResult("generic_api", status, settings.url, response.text[:500], _utc_now(), response.status_code)
        except Exception as exc:  # pragma: no cover - network path
            return DeliveryResult("generic_api", "FAILED_POST", settings.url, str(exc), _utc_now())


def _smtp_login(server: smtplib.SMTP, settings: SMTPSettings) -> None:
    if settings.username:
        server.login(settings.username, settings.password)


def _subject_for(planned: PlannedCelebration) -> str:
    employee = planned.event.employee
    if planned.event.event_type == "birthday":
        return f"Happy Birthday, {employee.preferred_name}!"
    years = planned.event.years or ""
    return f"Congratulations on your {years}-year work anniversary, {employee.preferred_name}!"


def _email_body(planned: PlannedCelebration, message: str) -> str:
    event = planned.event
    return (
        f"Hello {event.employee.preferred_name},\n\n"
        f"{message}\n\n"
        f"Event: {event.event_type}\n"
        f"Event Date: {planned.event_date.isoformat()}\n"
        f"Department: {event.employee.department}\n\n"
        "Regards,\nAI Employee Celebration Agent\n"
    )


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _csv_env(name: str) -> list[str]:
    raw = os.getenv(name, "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def _json_env(name: str, default: dict[str, str]) -> dict[str, str]:
    raw = os.getenv(name)
    if not raw:
        return default
    parsed = json.loads(raw)
    return {str(key): str(value) for key, value in parsed.items()}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
